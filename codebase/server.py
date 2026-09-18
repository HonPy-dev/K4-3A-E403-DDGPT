#!/usr/bin/env python3
"""VLearn Ready — 1 server chay that cho demo (static + API proxy DeepSeek).

Chay (cmd, tai thu muc repo):
    set DEEPSEEK_API_KEY=... & python server.py [--port 3000]
Mo: http://localhost:3000  (dashboard), /reader.html, /vlearn_ready_mock.html

Endpoints:
    GET  /api/health   -> {key: bool, fixtures: n, cases: n} (khong ton tien)
    POST /api/prep     {lesson} -> Prep JSON live (paste 4 fixture, temp 0.2,
                         ep JSON, validate allowlist) + luu trace
    POST /api/ask      {case_id} -> chay 1 case golden (prompt tu eval/tests.csv)
    GET  /api/metrics  -> doc eval/metrics.json (so do Giang chot) cho tab So do

Bao mat: key CHI doc tu bien moi truong, KHONG log key, KHONG commit key.
Mat mang/het key -> API tra 502 + frontend tu fallback Prep cache (da validate).
Chi dung stdlib (khong pip install).
"""
import csv
import datetime
import importlib.util
import json
import os
import sys
import urllib.parse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
AI_DIR = os.path.join(ROOT, "ai")
EVAL_DIR = os.path.join(ROOT, "eval")
TRACES = os.path.join(EVAL_DIR, "traces")
METRICS = os.path.join(EVAL_DIR, "metrics.json")
TESTS_CSV = os.path.join(EVAL_DIR, "tests.csv")


def _load_dotenv():
    # Doc key tu .env (cung thu muc repo) neu chua co env — .env da gitignore.
    # Khong bao gio in/log key.
    p = os.path.join(ROOT, ".env")
    if not os.path.exists(p):
        return
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


_load_dotenv()


def _load_ai():
    spec = importlib.util.spec_from_file_location(
        "ai_call", os.path.join(AI_DIR, "ai_call.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AI = _load_ai()


def _key():
    return os.environ.get("DEEPSEEK_API_KEY")


def _tests():
    with open(TESTS_CSV, encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def _trace(name, obj):
    os.makedirs(TRACES, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = os.path.join(TRACES, "api-live-%s-%s.json" % (ts, name))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    return path


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, *a):
        pass  # giu log sach cho demo (loi van in ra stderr qua send_error)

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = 0
        raw = self.rfile.read(n) if n else b"{}"
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/health":
            tests = _tests()
            with open(os.path.join(AI_DIR, "lessons.json"), encoding="utf-8") as f:
                live = sorted(json.load(f)["lessons"].keys())
            return self._json(200, {
                "ok": True,
                "key_present": bool(_key()),
                "live_lessons": live,
                "cases": len([i for i in tests if i not in AI.SKIP_IDS]),
                "note": "health khong goi AI (khong ton tien). Test live: POST /api/prep {lesson:'T06'}",
            })
        if path == "/api/metrics":
            if os.path.exists(METRICS):
                with open(METRICS, encoding="utf-8") as f:
                    return self._json(200, json.load(f))
            return self._json(200, {"updated_at": None,
                                    "note": "chua co so do — Giang chay ai/run_eval.py --all roi cap nhat"})
        if path.startswith("/_next/") or path.startswith("/brand/"):
            # Asset chet tu ban export Next.js (font/logo cu) — tra 204 cho sach log demo.
            # Font tu fallback ve system, khong anh huong UI.
            self.send_response(204)
            self.end_headers()
            return
        return super().do_GET()

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path not in ("/api/prep", "/api/ask"):
            return self._json(404, {"ok": False, "error": "unknown endpoint"})
        key = _key()
        if not key:
            return self._json(502, {"ok": False, "error": "THIEU KEY (set DEEPSEEK_API_KEY)",
                                    "fallback": "frontend dung Prep cache da validate"})
        try:
            if path == "/api/prep":
                # Prep AI live theo lesson trong registry (ai/lessons.json).
                # Bai khac -> frontend giu mock tinh + banner noi ro (trung thuc).
                data = self._body()
                lesson = (data.get("lesson") or "L6").strip().upper()
                try:
                    spec = AI.load_lesson(lesson)
                except KeyError:
                    with open(os.path.join(AI_DIR, "lessons.json"), encoding="utf-8") as f:
                        live = sorted(json.load(f)["lessons"].keys())
                    return self._json(200, {"ok": False, "reason": "chua-co-fixture",
                                            "lesson": data.get("lesson"),
                                            "live_lessons": live,
                                            "note": "Bai nay chua co nguon Tier-1 — dung ban mock tinh"})
                sources, allow = spec["sources"], spec["allow"]
                prompt = AI.build_prompt(sources, spec["base_question"], spec["system"])
                name, label = "prep-" + lesson, lesson
                strict = spec.get("strict_codes", True)
            else:
                # Golden Cxx chay tren fixture L6 (registry) — khong phu thuoc file cu.
                data = self._body()
                row = _tests().get(data.get("case_id", ""))
                if not row or row["id"] in AI.SKIP_IDS:
                    return self._json(400, {"ok": False, "error": "case_id khong hop le"})
                l6 = AI.load_lesson("L6")
                sources, allow = l6["sources"], l6["allow"]
                prompt = AI.build_prompt(sources, row["prompt"], l6["system"])
                name, label = row["id"], row["id"]
                strict = l6.get("strict_codes", True)
            # AI nondeterministic: rot validate format -> goi lai (toi da 3 lan),
            # tra ve ban PASS dau tien. Luu trace moi lan thu (trung thuc).
            errs, parsed, raw, tpath, attempt = ["chua goi AI"], None, "", None, 0
            transport_errors = []
            for attempt in (1, 2, 3):
                try:
                    raw = AI.call_deepseek(key, prompt)
                except Exception as e:
                    message = "AI call that bai (lan %d): %s" % (attempt, e)
                    transport_errors.append(message)
                    errs = [message]
                    continue
                try:
                    parsed = json.loads(raw)
                except Exception:
                    parsed = {"_parse_error": True, "_raw_head": (raw or "")[:300]}
                errs = AI.validate(parsed, allow, strict)
                trace = {"transport": "server-live", "model": AI.DS_MODEL,
                         "case": label, "attempt": attempt,
                         "prompt": prompt, "raw_text": raw,
                         "parsed": parsed, "validation": {"ok": not errs, "errors": errs}}
                tpath = _trace("%s-r%d" % (name, attempt), trace)
                if not errs:
                    break
            # Loi transport/auth/quota khong phai loi schema. Tra 502 de UI va
            # nguoi van hanh phan biet voi 422 (AI co response nhung sai format).
            if parsed is None and transport_errors:
                return self._json(502, {"ok": False,
                                        "error": transport_errors[-1],
                                        "attempts": attempt,
                                        "hint": "Kiem tra DEEPSEEK_API_KEY, quota va provider; restart server sau khi sua key.",
                                        "fallback": "frontend dung Prep cache da validate"})
            return self._json(200 if not errs else 422,
                              {"ok": not errs, "errors": errs, "data": parsed,
                               "attempts": attempt,
                               "trace": os.path.basename(tpath) if tpath else None})
        except Exception as e:  # mang hong / rate-limit / het tien
            return self._json(502, {"ok": False, "error": "AI call that bai: %s" % e,
                                    "fallback": "frontend dung Prep cache da validate"})


def main(argv):
    port = 3000
    for i, a in enumerate(argv):
        if a == "--port" and i + 1 < len(argv):
            port = int(argv[i + 1])
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print("VLearn Ready LIVE: http://localhost:%d  (Ctrl+C de dung)" % port)
    print("/api/health de kiem tra truoc gio demo.")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main(sys.argv[1:])

#!/usr/bin/env python3
"""VLearn Ready — chay so do CP3 QUA DUNG DUONG DEMO (server.py -> DeepSeek).

Dung:
    1. Cua so 1:  set DEEPSEEK_API_KEY=... & python server.py
    2. Cua so 2:  python ai\\run_eval.py --all        (20 case, ~10 phut)
                  python ai\\run_eval.py --only C01,C11
    3. Cham F/C/R vao eval\\results-run-live.md, roi chot so:
                  python ai\\run_eval.py --metrics 100 75 95 --run run-live-1
       -> ghi eval\\metrics.json, tab So do tren modal tu hien.

Trace moi case luu tai eval\\traces\\ (server tu luu, ten api-live-*.json).
"""
import csv
import datetime
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_CSV = os.path.join(ROOT, "eval", "tests.csv")
METRICS = os.path.join(ROOT, "eval", "metrics.json")
BASE_URL = os.environ.get("VLEARN_API", "http://localhost:3000")
SKIP = {"C19", "C22"}  # C19 tay (dilution NotebookLM), C22 test tren UI


def _post(path, obj, timeout=120):
    req = urllib.request.Request(
        BASE_URL + path, data=json.dumps(obj).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def main(argv):
    if "--metrics" in argv:
        i = argv.index("--metrics")
        f, c, r = argv[i + 1:i + 4]
        run = "run-live-1"
        for j, a in enumerate(argv):
            if a == "--run" and j + 1 < len(argv):
                run = argv[j + 1]
        with open(METRICS, "w", encoding="utf-8") as fh:
            json.dump({"updated_at": datetime.date.today().isoformat(), "run": run,
                       "transport": "server.py -> deepseek-chat", "n": 20,
                       "f_pct": int(f), "c_pct": int(c), "r_pct": int(r),
                       "note": "Chi tiet tung case: eval/results-run-live.md. "
                               "NotebookLM giu lam evidence so sanh (ask-02, C11, dilution)."},
                      fh, ensure_ascii=False, indent=1)
        print("da ghi", METRICS)
        return 0
    only = None
    for a in argv:
        if a == "--only" or a.startswith("--only="):
            only = (a.split("=", 1)[1] if "=" in a else argv[argv.index(a) + 1]).split(",")
    with open(TESTS_CSV, encoding="utf-8") as fh:
        rows = [x for x in csv.DictReader(fh) if x["id"] not in SKIP]
    n_ok = 0
    for row in rows:
        if only is not None and row["id"] not in only:
            continue
        try:
            res = _post("/api/ask", {"case_id": row["id"]})
            ok = bool(res.get("ok"))
            n_ok += ok
            print("[%s] server-validation=%s %s trace=%s" %
                  (row["id"], "PASS" if ok else "FAIL", res.get("errors"), res.get("trace")))
        except Exception as e:
            print("[%s] ERROR: %s" % (row["id"], e))
        time.sleep(10)
    print("XONG: %d PASS validation (format). Cham F/C/R vao results-run-live.md." % n_ok)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

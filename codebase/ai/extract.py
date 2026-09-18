#!/usr/bin/env python3
"""VLearn Ready — trich excerpt DATA THAT (transcript + slide) cho Prep AI live.

Khong chatlog. Chi excerpt ngan (bao mat data pack: khong commit file goc).
Citation that giu nguyen: [Txx-NNN] trong transcript, [slide N] cho slide.

Dung:
    python ai\\extract.py --stats                 (xem cau truc, khong ghi file)
    python ai\\extract.py --lesson T06            (ghi eval\\fixtures\\lesson-T06.json)

Quy uoc fixture ra: {"lesson":..., "sources":[{"id","title","text"}]}
  - id T06/T04: text gom cac segment giu nguyen ma [Txx-NNN] de AI cite that.
  - id SLIDE: text gom cac slide giu nguyen [slide N].
Tong ~25-30K ky tu (vua context DeepSeek, tranh dilution).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = r"D:\Coding\Lab\Hackathon\K4-3A-Day05-06-AI-Product-Hackathon\data\vlearn-pack"
OUT = os.path.join(ROOT, "eval", "fixtures")

LESSONS = {
    "T06": {
        "title": "Buoi Foundation: transformer & attention",
        "target": {"file": "transcript-06-clean.md",
                   "sections": ["Transformer", "Self-attention", "Token"],
                   "cap": 40},
        "sources": [
            {"id": "T04", "title": "T04 token/attention/LLM nen",
             "file": "transcript-04-clean.md",
             "keywords": ["next token", "doan token", "attention", "xac suat", "probability"],
             "exclude": ["hold token", "đồng token", "dong token", "crypto", "blockchain", "coin", "kid plaza", "viec lam"],
             "cap": 20},
            {"id": "SLIDE", "title": "Slide Day1 transformer/token",
             "keywords": ["token", "transformer", "attention", "embedding", "xac suat", "probability"],
             "cap": 8},
        ],
    },
}


def parse_transcript(path):
    """-> [(seg_id, section, text)] (bo dong tieu de file)."""
    raw = open(path, encoding="utf-8").read()
    out, section, cur_id, buf = [], "", None, []
    def flush():
        if cur_id and buf:
            out.append((cur_id, section, " ".join(buf).strip()))
    for line in raw.splitlines():
        m = re.match(r"##\s+(.*)", line)
        if m:
            flush(); cur_id, buf = None, []; section = m.group(1).strip(); continue
        for sm in re.finditer(r"\[(T\d{2}-\d+)\]", line):
            flush(); cur_id, buf = sm.group(1), []
        if cur_id:
            buf.append(re.sub(r"\[T\d{2}-\d+\]", "", line).strip())
    flush()
    return [(i, s, re.sub(r"\s+", " ", t)) for i, s, t in out if len(t) > 20]


def pick(segs, sections=None, keywords=None, cap=20, skip_class=True, exclude=None):
    res = []
    for i, s, t in segs:
        if skip_class and t.startswith("[Hoạt động lớp"):
            continue
        low = t.lower()
        if exclude and any(k.lower() in low for k in exclude):
            continue
        ok_sec = sections and any(k.lower() in s.lower() for k in sections)
        ok_kw = keywords and any(k.lower() in low for k in keywords)
        if (sections or keywords) and not (ok_sec or ok_kw):
            continue
        res.append((i, s, t))
        if len(res) >= cap:
            break
    return res


def slide_pages():
    import fitz
    out = []
    for f in ["d1-slide-hackathon.pdf", "d2-slide-hackathon.pdf"]:
        d = fitz.open(os.path.join(DATA, "slides", f))
        for i, p in enumerate(d):
            t = re.sub(r"\s+", " ", (p.get_text() or "").strip())
            if len(t) > 80:
                out.append((f, i + 1, t))
    return out


def build_lesson(lid):
    spec = LESSONS[lid]
    tsegs = {f: parse_transcript(os.path.join(DATA, "transcript", f))
             for f in {spec["target"]["file"]} | {s["file"] for s in spec["sources"] if "file" in s}}
    t = spec["target"]
    tgt = pick(tsegs[t["file"]], sections=t["sections"], cap=t["cap"])
    sources = [{"id": lid, "title": "TARGET " + spec["title"],
                "text": "\n".join("[%s] (%s) %s" % (i, s, x) for i, s, x in tgt)}]
    for s in spec["sources"]:
        if "file" in s:
            items = pick(tsegs[s["file"]], keywords=s.get("keywords"), cap=s["cap"],
                         exclude=s.get("exclude"))
            text = "\n".join("[%s] (%s) %s" % (i, sec, x) for i, sec, x in items)
        else:
            pages = [(f, n, x) for f, n, x in slide_pages()
                     if any(k.lower() in x.lower() for k in s["keywords"])][:s["cap"]]
            text = "\n".join("[slide %s/%d] %s" % (f[:2].upper(), n, x) for f, n, x in pages)
        sources.append({"id": s["id"], "title": s["title"], "text": text})
    return {"lesson": lid, "title": spec["title"], "note": "Excerpt that (khong full file).", "sources": sources}


def main(argv):
    if "--stats" in argv:
        for f in ["transcript-04-clean.md", "transcript-06-clean.md"]:
            segs = parse_transcript(os.path.join(DATA, "transcript", f))
            print(f, "segments:", len(segs), "chars:", sum(len(t) for _, _, t in segs))
        print("slide pages:", len(slide_pages()))
        return 0
    lid = "T06"
    for i, a in enumerate(argv):
        if a == "--lesson" and i + 1 < len(argv):
            lid = argv[i + 1]
    fx = build_lesson(lid)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "lesson-%s.json" % lid)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(fx, f, ensure_ascii=False, indent=1)
    total = sum(len(s["text"]) for s in fx["sources"])
    for s in fx["sources"]:
        print("%s: %d chars" % (s["id"], len(s["text"])))
    print("TOTAL %d chars -> %s" % (total, path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

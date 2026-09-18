#!/usr/bin/env python3
"""VLearn Ready CP3 — kiem tra trace NotebookLM truoc khi dong bang prep-cp3.json.

Dung:
    python convert_trace.py eval\\traces\\ask-02-targeted-pass.json
    python convert_trace.py eval\\traces\\C01.json --emit-skeleton

Viec script lam (deterministic, khong goi AI):
  1. Doc trace JSON cua `ask --json`.
  2. Bao FAIL neu: khong co references (= nguy co bia / false refusal),
     source_id la ngoai 4 fixture, answer rong.
  3. --emit-skeleton: sinh khung prep JSON de nguoi dien thu cong tu answer
     (human-in-the-loop = dung kieu Conditional theo spec §14).

4 fixture ID chot cho dot CP3 (doi o day neu doi notebook):
"""
import json
import sys

FIXTURES = {
    "8ba0b78d-65b5-4b1f-8107-767426ec1f4a": "L6-target-RAG-reranking",
    "0728fb48-a29b-43b4-9027-a62c7245cfb7": "L3-embedding-1840",
    "901a319c-bf33-4d36-a506-cbcf2af75f00": "L4-chunking-slide14-17",
    "b6b02d81-acee-4a9d-b2e9-ce4fb4628f5f": "instructor-intent-L6",
}


def main(path, emit=False):
    with open(path, encoding="utf-8") as f:
        trace = json.load(f)
    answer = trace.get("answer", "")
    refs = trace.get("references", []) or []
    errors = []
    if not answer.strip():
        errors.append("answer rong")
    if not refs:
        errors.append("KHONG co references -> nguy co bia hoac false refusal, LOAI")
    strange = [r.get("source_id") for r in refs if r.get("source_id") not in FIXTURES]
    if strange:
        errors.append("citation ngoai fixture: %s" % strange)
    print("== TRACE:", path)
    print("answer chars:", len(answer))
    print("references:", [(r.get("citation_number"), FIXTURES.get(r.get("source_id"), "?")) for r in refs])
    if errors:
        print("KET LUAN: FAIL -", "; ".join(errors))
        return 1
    print("KET LUAN: PASS - du dieu kien dong bang prep-cp3.json")
    if emit:
        skel = {
            "lesson": "Lesson 6 · RAG + Reranking",
            "outcomes": ["<dien tu answer>"],
            "prereqs": [{"id": "<emb|chunk|...>", "name": "<ten>", "label": "<Required|Helpful|Taught-in-lesson>",
                         "evidence": "<trich answer>", "source": "<1 trong 4 fixture>", "review": "<route 1 nguon>"}],
            "questions": [{"id": "q1", "prereq_id": "<id>", "stem": "<cau hoi>", "options": [],
                           "answer": "<A|B|C>", "source_ref": "<nguon>"}],
        }
        print(json.dumps(skel, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], emit="--emit-skeleton" in sys.argv))

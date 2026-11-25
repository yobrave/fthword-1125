import json
import os
from pathlib import Path

LIMIT = 24
STAGE = "first-thought"
SEPARATOR = " "  # entries must be a single token; any split means reject

def inspect(raw_bytes):
    text = raw_bytes.decode("utf-8").strip()
    tokens = [t for t in text.split(SEPARATOR) if t]
    return {"word": text, "chars": len(text), "tokens": len(tokens)}

def main():
    home = Path(__file__).resolve().parent
    facts = inspect((home / "entry.txt").read_bytes())
    passed = 0 < facts["chars"] <= LIMIT and facts["tokens"] == 1
    receipt = {"stage": STAGE, "gate": passed, "chars": facts["chars"], "tokens": facts["tokens"], "word": facts["word"]}
    if passed:
        target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
        target.mkdir(parents=True, exist_ok=True)
        (target / "entry.txt").write_bytes((home / "entry.txt").read_bytes())
    print(json.dumps(receipt, ensure_ascii=False))
    raise SystemExit(0 if passed else 1)

main()

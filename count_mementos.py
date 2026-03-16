from __future__ import annotations
import json
from pathlib import Path
from collections import Counter

TIMEMAP_DIR = Path("../timemaps")

def count_mementos_in_file(path: Path) -> int:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return 0

    if isinstance(data, dict) and "mementos" in data:
        m = data["mementos"]
        if isinstance(m, dict) and "list" in m and isinstance(m["list"], list):
            return len(m["list"])

    return 0

def main() -> None:
    counts = []

    for f in TIMEMAP_DIR.glob("*.json"):
        counts.append(count_mementos_in_file(f))

    freq = Counter(counts)

    print("Mementos,URI-Rs")
    for memento_count in sorted(freq):
        print(f"{memento_count},{freq[memento_count]}")

    if counts:
        print()
        print("Maximum mementos:", max(counts))

if __name__ == "__main__":
    main()
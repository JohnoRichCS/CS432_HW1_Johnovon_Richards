from __future__ import annotations
import hashlib
import json
from pathlib import Path

URI_FILE = Path("../uris.txt")
TIMEMAP_DIR = Path("../timemaps")

def md5_name(uri: str) -> str:
    return hashlib.md5(uri.encode("utf-8")).hexdigest()

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
    uris = [line.strip() for line in URI_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]

    pairs = []
    for uri in uris:
        filename = TIMEMAP_DIR / f"{md5_name(uri)}.json"
        count = count_mementos_in_file(filename)
        pairs.append((count, uri))

    pairs.sort(reverse=True)

    print("Top 10 URI-Rs by memento count:\n")
    for count, uri in pairs[:10]:
        print(f"{count:5d}  {uri}")

if __name__ == "__main__":
    main()
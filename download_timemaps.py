from __future__ import annotations
import hashlib
import subprocess
import time
from pathlib import Path

MEMGATOR = Path("../memgator.exe")
CONTACT = "johnovonwork@gmail.com"
ARCHIVES = "https://raw.githubusercontent.com/odu-cs432-websci/public/main/archives.json"

URI_FILE = Path("../uris.txt")
OUTDIR = Path("../timemaps")
OUTDIR.mkdir(exist_ok=True)

def md5_name(uri: str) -> str:
    return hashlib.md5(uri.encode("utf-8")).hexdigest()

def main() -> None:
    uris = [line.strip() for line in URI_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]

    for i, uri in enumerate(uris, start=1):
        name = md5_name(uri)
        outfile = OUTDIR / f"{name}.json"

        print(f"[{i}/{len(uris)}] {uri}")

        with open(outfile, "w", encoding="utf-8") as out:
            subprocess.run(
                [
                    str(MEMGATOR),
                    "-c", CONTACT,
                    "-a", ARCHIVES,
                    "-f", "JSON",
                    "-k", "5",
                    uri,
                ],
                stdout=out,
                stderr=subprocess.DEVNULL,
                text=True,
                check=False,
            )

        time.sleep(5)

if __name__ == "__main__":
    main()
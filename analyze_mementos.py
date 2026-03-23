from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone
import matplotlib.pyplot as plt

TIMEMAP_DIR = Path("../timemaps")

def get_mementos(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except:
        return []

    if "mementos" in data and "list" in data["mementos"]:
        return data["mementos"]["list"]

    return []

def main():
    ages = []
    counts = []

    today = datetime.now(timezone.utc)

    for file in TIMEMAP_DIR.glob("*.json"):
        mementos = get_mementos(file)

        if len(mementos) == 0:
            continue

        count = len(mementos)

        dates = []
        for m in mementos:
            try:
                dt = datetime.fromisoformat(m["datetime"].replace("Z", "+00:00"))
                dates.append(dt)
            except:
                continue

        if not dates:
            continue

        earliest = min(dates)

        age_days = (today - earliest).days

        ages.append(age_days)
        counts.append(count)

    plt.figure()
    plt.scatter(ages, counts)
    plt.xlabel("Age in Days")
    plt.ylabel("Number of Mementos")
    plt.title("Age vs Number of Mementos")

    plt.savefig("../scatterplot.png")
    plt.show()

if __name__ == "__main__":
    main()
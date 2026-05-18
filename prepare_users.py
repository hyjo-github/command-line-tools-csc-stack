#!/usr/bin/env python3

from pathlib import Path
import csv

INPUT_DIR = Path("files") / "submissions"
OUTPUT_CSV = Path("files") / "students.csv"
OUTPUT_MAP = Path("files") / "mapping.txt"

rows = []
counter = 1

for folder in sorted([p for p in INPUT_DIR.iterdir() if p.is_dir()]):
    pubkey = None
    for f in [p for p in folder.iterdir() if p.suffix == ".pub"]:
        pubkey = f.read_text().strip()
        break
    if not pubkey:
        continue

    username = f"student{counter:04d}"
    rows.append({"username": username, "moodle_id": folder.name, "pubkey": pubkey})

    counter += 1

with OUTPUT_CSV.open("w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["username", "pubkey"])
    writer.writeheader()
    for r in rows:
        writer.writerow({"username": r["username"], "pubkey": r["pubkey"]})

with OUTPUT_MAP.open("w") as f:
    for r in rows:
        f.write(f"{r['moodle_id']} → {r['username']}\n")

print(f"Created {OUTPUT_CSV} and {OUTPUT_MAP}")

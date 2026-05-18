#!/usr/bin/env python3

from pathlib import Path
import csv

INPUT_DIR = Path("files") / "submissions"
OUTPUT_CSV = Path("files") / "students.csv"
OUTPUT_MAP = Path("files") / "mapping.txt"

rows = []
existing_users = {}
counter = 1

if OUTPUT_CSV.exists():
    with OUTPUT_CSV.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_users[row["moodle_id"]] = row

def extract_number(username: str) -> int:
    return int(username.replace("student", ""))

if existing_users:
    counter = max(extract_number(u["username"]) for u in existing_users.values()) + 1

for folder in sorted([p for p in INPUT_DIR.iterdir() if p.is_dir()]):
    pubkey = None
    for f in [p for p in folder.iterdir() if p.suffix == ".pub"]:
        pubkey = f.read_text().strip()
        break
    if not pubkey:
        continue

    # If user already exists, re-use
    if folder.name in existing_users:
        row = existing_users[folder.name]
        # Update key if changed
        row["pubkey"] = pubkey
    else:
        username = f"student{counter:04d}"
        row = {
            "username": username, 
            "moodle_id": folder.name, 
            "pubkey": pubkey
            }
        existing_users[folder.name] = row
        counter += 1

    rows.append(row)

with OUTPUT_CSV.open("w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["moodle_id", "username", "pubkey"])
    writer.writeheader()
    writer.writerows(rows)

with OUTPUT_MAP.open("w") as f:
    for r in rows:
        f.write(f"{r['moodle_id']} → {r['username']}\n")

print(f"Created {OUTPUT_CSV} and {OUTPUT_MAP}")

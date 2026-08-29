import os
import json
import csv
from idlelib import __main__

from fastapi import HTTPException

def file_last_change(path) -> float | None:
    file = path.split("/")[-1]
    try:
        last_change = os.stat(path).st_mtime
        return last_change
    except (FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail=f"File {file} is unreachable")

def load_file(path, op):
    file = path.split("/")[-1]

    if op == "csv":
        res = []
        try:
            with open(path, 'r', newline='') as stats_file:
                reader = csv.DictReader(stats_file)
                for row in reader:
                    res.append(row)

                return res
        except (FileNotFoundError, IOError):
            raise HTTPException(status_code=500, detail=f"File {file} is unreachable")
    elif op == "json":
        try:
            with open(path, 'r', newline='') as stats_file:
                reader = json.load(stats_file)
                return reader
        except (FileNotFoundError, IOError):
            raise HTTPException(status_code=500, detail=f"File {file} is unreachable")
    elif op == "aof":
        f_json = {}
        try:
            with open(path, mode='r', encoding='utf-8-sig') as f:
                for line in f:
                    word = line.split()
                    if len(word) < 2:
                        continue
                    f_json[int(word[0])] = word[1]
                return f_json
        except (FileNotFoundError, IOError):
            raise HTTPException(status_code=500, detail=f"File {file} is unreachable")
    else:
        raise ValueError(f"Unsupported file extension: {op}")


# Didn't want to make a separate utils.py file, so this is here
def get_all_player_stats_by_name(stats, name) -> dict[str, str] | None:
    for row in stats:
        if row['Player Name'] == name:
            return row
    raise HTTPException(status_code=404, detail=f"Stats with that player name not found")


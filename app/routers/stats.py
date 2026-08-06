from fastapi import APIRouter, HTTPException
from app.core import common
import csv
import json
import os

PATH_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/stats.json"))
PATH_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/stats.csv"))
router = APIRouter()

# -------- Helpers --------
def load_stats_json():
    try:
        with open(PATH_JSON, 'r', newline='') as stats_file:
            reader = json.load(stats_file)
            return reader
    except (FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail=f"Wasn't able to read stats.json")

def load_stats_csv():
    res = []
    try:
        with open(PATH_CSV, 'r', newline='') as stats_file:
            reader = csv.DictReader(stats_file)
            for row in reader:
                res.append(row)

            return res
    except (FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail=f"Wasn't able to read stats.csv file")

# JSON change tracking
last_change_json = common.file_last_change(PATH_JSON)
stats_json = load_stats_json()

def check_update_json():
    global stats_json, last_change_json
    current_change = common.file_last_change(PATH_JSON)
    if last_change_json != current_change:
        stats_json = load_stats_json()
        last_change_json = current_change

    return stats_json

# CSV change tracking
last_change_csv = common.file_last_change(PATH_CSV)
stats_csv = load_stats_csv()

def check_update_csv():
    global stats_csv, last_change_csv
    current_change = common.file_last_change(PATH_CSV)
    if last_change_csv != current_change:
        stats_csv = load_stats_csv()
        last_change_csv = current_change

    return stats_csv

# ------- Routers Start  ----------
@router.get('/stats/all', tags=['stats'])
def get_all_stats():
    stats = check_update_json()
    return stats['scoreboard']['scores']


@router.get('/stats/{uuid}/{stat_name}', tags=['stats'])
def get_player_stat_by_name(uuid: str, stat_name: str):
    stats = check_update_csv()

    for row in stats:
        if row['uuid'] == uuid and stat_name in row:
            return {"uuid": row['uuid'], "stat_value": row[stat_name]}
    raise HTTPException(status_code=404, detail=f"Account with that uuid not found or stat doesnt exist.")

@router.get('/stats/{uuid}', tags=['stats'])
def get_all_player_stats(uuid: str):
    stats = check_update_csv()

    for row in stats:
        if row['uuid'] == uuid:
            return row
    raise HTTPException(status_code=404, detail=f"Account with that uuid not found")

@router.get('/stats_name/{player_name}', tags=['stats'])
def get_all_player_stats_by_name(player_name: str):
    stats = check_update_csv()

    for row in stats:
        if row['Player Name'] == player_name:
            return row
    raise HTTPException(status_code=404, detail=f"Stats with that player name not found")


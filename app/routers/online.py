from fastapi import APIRouter, HTTPException
from app.core import common
import json
import os

from core.common import load_file

PATH_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/stats.json"))
PATH_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/stats.csv"))
router = APIRouter()

csv_stats = common.load_file(PATH_CSV, "csv")
csv_last_change = common.file_last_change(PATH_CSV)
def load_online():
    global csv_stats, csv_last_change
    current_csv_change = common.file_last_change(PATH_CSV)
    stats = common.load_file(PATH_CSV, "csv") if csv_last_change != current_csv_change else csv_stats

    try:
        with open(PATH_JSON, 'r', encoding='utf-8') as online_file:
            reader = json.load(online_file)
            player_names = list(reader['online'].keys())
            res = []

            for player_name in player_names:
                try:
                    player = common.get_all_player_stats_by_name(stats)
                    if player and ('uuid' in player):
                        res.append(player['uuid'])
                except Exception as e:
                    continue

            return res
    except(FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail="File is unreachable")

online = load_online()
last_change = common.file_last_change(PATH_JSON)
@router.get('/online', tags=["online"])
def get_online_players():
    global last_change, online
    current_change = common.file_last_change(PATH_JSON)

    if current_change != last_change:
        last_change = current_change
        online = load_online()

    return online

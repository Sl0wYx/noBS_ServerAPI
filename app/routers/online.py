from fastapi import APIRouter, HTTPException
from app.core import common
from app.routers.stats import get_all_player_stats_by_name
import json
import os

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/stats.json"))
router = APIRouter()

def load_online():
    try:
        with open(PATH, 'r', encoding='utf-8') as online_file:
            reader = json.load(online_file)
            player_names = list(reader['online'].keys())
            res = []

            for player_name in player_names:
                try:
                    player = get_all_player_stats_by_name(player_name)
                    if player and ('uuid' in player):
                        res.append(player['uuid'])
                except Exception as e:
                    continue

            return res
    except(FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail="File is unreachable")

online = load_online()
last_change = common.file_last_change(PATH)
@router.get('/online', tags=["online"])
def get_online_players():
    global last_change, online
    current_change = common.file_last_change(PATH)

    if current_change != last_change:
        last_change = current_change
        online = load_online()

    return online

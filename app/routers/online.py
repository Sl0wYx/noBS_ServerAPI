from fastapi import APIRouter
from app.core import common
from app.core.cache import FileCache
import os

PATH_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/stats.json"))
PATH_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/stats.csv"))
router = APIRouter()

csv_stats = common.load_file(PATH_CSV, "csv")
csv_last_change = common.file_last_change(PATH_CSV)
csv_cache = FileCache(PATH_CSV, csv_stats, "csv", csv_last_change)

json_stats = common.load_file(PATH_JSON, "json")
json_last_change = common.file_last_change(PATH_JSON)
json_cache = FileCache(PATH_JSON, json_stats, "json", json_last_change)

def load_online() -> list[str]:
    csv_cache.check()
    json_cache.check()

    player_names = list(json_cache.data['online'].keys())
    res = []

    for player_name in player_names:
        try:
            player = common.get_all_player_stats_by_name(csv_cache.data, player_name)
            if player and ('uuid' in player):
                res.append(player['uuid'])
        except Exception as e:
            continue

    return res

online = load_online()
online_last_change = common.file_last_change(PATH_JSON)
@router.get('/online', tags=["online"])
def get_online_players() -> list[str]:
    global online_last_change, online
    current_change = common.file_last_change(PATH_JSON)

    if current_change != online_last_change:
        online_last_change = current_change
        online = load_online()

    return online

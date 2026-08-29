from fastapi import APIRouter, HTTPException
from app.core import common
from app.core.cache import FileCache
import os

PATH_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/stats.json"))
PATH_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/stats.csv"))
router = APIRouter()

# JSON change tracking
last_change_json = common.file_last_change(PATH_JSON)
stats_json = common.load_file(PATH_JSON, "json")
json_cache = FileCache(PATH_JSON, stats_json, "json", last_change_json)

# CSV change tracking
last_change_csv = common.file_last_change(PATH_CSV)
stats_csv = common.load_file(PATH_CSV, "csv")
csv_cache = FileCache(PATH_CSV, stats_csv, "csv", last_change_csv)

# ------- Routers Start  ----------
@router.get('/stats/all', tags=['stats'])
def get_all_stats() -> dict:
    json_cache.check()
    return json_cache.data['scoreboard']['scores']

@router.get('/stats/player/uuid/{uuid}/{stat_name}', tags=['stats'])
def get_player_stat_by_name(uuid: str, stat_name: str) -> dict[str, str] | None:
    csv_cache.check()

    for row in csv_cache.data:
        if row['uuid'] == uuid and stat_name in row:
            return {"uuid": row['uuid'], "stat_value": row[stat_name]}
    raise HTTPException(status_code=404, detail=f"Account with that uuid not found or stat doesnt exist.")

@router.get('/stats/player/uuid/{uuid}', tags=['stats'])
def get_all_player_stats(uuid: str) -> dict[str, str] | None:
    csv_cache.check()

    for row in csv_cache.data:
        if row['uuid'] == uuid:
            return row
    raise HTTPException(status_code=404, detail=f"Account with that uuid not found")

@router.get('/stats/player/name/{player_name}', tags=['stats'])
def get_all_player_stats_by_name(player_name: str) -> dict[str, str] | None:
    csv_cache.check()
    return common.get_all_player_stats_by_name(csv_cache.data, player_name)

@router.get('/stats/metrics/death_rate', tags=['stats'])
def get_death_rate() -> dict[str, dict[str, float]] | None:
    json_cache.check()
    scores = json_cache.data['scoreboard']['scores']

    deaths_rate_stats = {'Death Rate': {}}

    for player in scores['Deaths'].keys():
        hours_played = int(scores['Hours Played'][player])
        deaths = int(scores['Deaths'][player])
        if (hours_played < 24 and deaths < 1) or hours_played == 0:
            continue

        deaths_per_hour = round(deaths / hours_played, 2)
        deaths_rate_stats['Death Rate'][player] = deaths_per_hour

    return deaths_rate_stats

@router.get('/stats/metrics/total_hours', tags=['stats'])
def get_total_hours() -> dict[str, int]:
    json_cache.check()
    hours_played = json_cache.data['scoreboard']['scores']['Hours Played']

    total_hours = 0
    for score in hours_played.values():
        total_hours += int(score)

    return {"Total Hours": total_hours}

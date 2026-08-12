from fastapi import APIRouter, HTTPException
from app.core import common
import os

PATH_JSON = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/stats.json"))
PATH_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/stats.csv"))
router = APIRouter()

# JSON change tracking
last_change_json = common.file_last_change(PATH_JSON)
stats_json = common.load_file(PATH_JSON, "json")

def check_update_json():
    global stats_json, last_change_json
    current_change = common.file_last_change(PATH_JSON)
    if last_change_json != current_change:
        stats_json = common.load_file(PATH_JSON, "json")
        last_change_json = current_change

    return stats_json

# CSV change tracking
last_change_csv = common.file_last_change(PATH_CSV)
stats_csv = common.load_file(PATH_CSV, "csv")

def check_update_csv():
    global stats_csv, last_change_csv
    current_change = common.file_last_change(PATH_CSV)
    if last_change_csv != current_change:
        stats_csv = common.load_file(PATH_CSV, "csv")
        last_change_csv = current_change

    return stats_csv

# ------- Routers Start  ----------
@router.get('/stats/all', tags=['stats'])
def get_all_stats():
    stats = check_update_json()
    return stats['scoreboard']['scores']


@router.get('/stats/player/uuid/{uuid}/{stat_name}', tags=['stats'])
def get_player_stat_by_name(uuid: str, stat_name: str):
    stats = check_update_csv()

    for row in stats:
        if row['uuid'] == uuid and stat_name in row:
            return {"uuid": row['uuid'], "stat_value": row[stat_name]}
    raise HTTPException(status_code=404, detail=f"Account with that uuid not found or stat doesnt exist.")

@router.get('/stats/player/uuid/{uuid}', tags=['stats'])
def get_all_player_stats(uuid: str):
    stats = check_update_csv()

    for row in stats:
        if row['uuid'] == uuid:
            return row
    raise HTTPException(status_code=404, detail=f"Account with that uuid not found")

@router.get('/stats/player/name/{player_name}', tags=['stats'])
def get_all_player_stats_by_name(player_name: str):
    stats = check_update_csv()
    return common.get_all_player_stats_by_name(stats, player_name)

@router.get('/stats/metrics/death_rate', tags=['stats'])
def get_death_rate():
    scores = check_update_json()['scoreboard']['scores']

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
def get_total_hours():
    hours_played = check_update_json()['scoreboard']['scores']['Hours Played']

    total_hours = 0
    for score in hours_played.values():
        total_hours += int(score)

    return {"Total Hours": total_hours}


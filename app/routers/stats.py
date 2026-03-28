from fastapi import APIRouter, HTTPException
import csv
import json

router = APIRouter()

@router.get('/stats/all', tags=['stats'])
def get_raw_stats():
    try:
        with open('app/data/stats.json', 'r', newline='') as stats_file:
            reader = json.load(stats_file)
            return reader['scoreboard']['scores']
    except (FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail=f"Wasn't able to read stats.json")

@router.get('/stats/{uuid}/{stat_name}', tags=['stats'])
def get_player_stat_by_name(uuid: str, stat_name: str):
    try:
        with open('app/data/stats.csv', 'r', newline='') as stats_file:
            reader = csv.DictReader(stats_file)
            for row in reader:
                for col in row:
                    if row['uuid'] == uuid and col == stat_name:
                        return {"uuid" : row['uuid'], "stat_value" : row[col]}

            raise HTTPException(status_code=404, detail=f"Stats not found")
    except (FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail=f"Wasn't able to read stats file")

@router.get('/stats/{uuid}', tags=['stats'])
def get_all_player_stats(uuid: str):
    try:
        with open('app/data/stats.csv', 'r', newline='') as stats_file:
            reader = csv.DictReader(stats_file)
            for row in reader:
                if row['uuid'] == uuid:
                    return row

            raise HTTPException(status_code=404, detail=f"Account with that uuid not found")
    except (FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail="Wasn't able to read stats file")

@router.get('/stats_name/{player_name}', tags=['stats'])
def get_all_player_stats_by_name(player_name: str):
    try:
        with open('app/data/stats.csv', 'r', newline='') as stats_file:
            reader = csv.DictReader(stats_file)
            for row in reader:
                if row['Player Name'] == player_name:
                    return row
            raise HTTPException(status_code=404, detail=f"Stats with that player name not found")

    except (FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail="Wasn't able to read stats file")
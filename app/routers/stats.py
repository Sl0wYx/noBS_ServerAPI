from fastapi import APIRouter
import csv

router = APIRouter()

@router.get('/stats/{uuid}/{stat_name}', tags=['stats'])
def get_player_stat_by_name(uuid: str, stat_name: str):
    with open('data/stats.csv', 'r', newline='') as stats_file:
        reader = csv.DictReader(stats_file)
        for row in reader:
            for col in row:
                if row['uuid'] == uuid and col == stat_name:
                    return {"uuid" : row['uuid'], "stat_value" : row[col]}

        return {"Error": "Either account with that UUID does not exist or stat name is wrong"}

@router.get('/stats/{uuid}', tags=['stats'])
def get_all_player_stats(uuid: str):
    with open('data/stats.csv', 'r', newline='') as stats_file:
        reader = csv.DictReader(stats_file)
        for row in reader:
            if row['uuid'] == uuid:
                return row

        return {"Error": "Account with that UUID does not exist"}

@router.get('/stats_name/{player_name}', tags=['stats'])
def get_all_player_stats_by_name(player_name: str):
    with open('data/stats.csv', 'r', newline='') as stats_file:
        reader = csv.DictReader(stats_file)
        for row in reader:
            if row['Player Name'] == player_name:
                return row
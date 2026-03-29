from fastapi import APIRouter, HTTPException
import json
from app.routers.stats import get_all_player_stats_by_name


router = APIRouter()


@router.get('/online', tags=["online"])
def get_online_players():
    try:
        with open('app/data/stats.json', 'r', encoding='utf-8') as online_file:
            reader = json.load(online_file)
            player_names = list(reader['online'].keys())
            online = set()

            for player_name in player_names:
                try:
                    player = get_all_player_stats_by_name(player_name)
                    if player and ('uuid' in player):
                        online.add(player['uuid'])
                except Exception as e:
                    continue


            return online

    except(FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail="File is unreachable")
from fastapi import APIRouter
import json

router = APIRouter()

@router.get('/online')
def get_online_players():
    with open('stats.json', 'r', encoding='utf-8') as online_file:
        reader = json.load(online_file)
        return reader['online'] # player_name:	true/false

from fastapi import APIRouter, HTTPException
from app.core import common
import os

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/accounts.aof"))
router = APIRouter()

accounts =  common.load_file(PATH, "aof")
last_change = common.file_last_change(PATH)
@router.get('/accounts/{discord_id}', tags=['accounts'])
def get_account(discord_id: int):
    global accounts, last_change
    current_change = common.file_last_change(PATH)

    if current_change != last_change:
        last_change = current_change
        accounts = common.load_file(PATH, "aof")

    if discord_id in accounts:
        return {
                "PlayerUUID": accounts[discord_id],
                "DiscordID": discord_id
                }
    else:
        raise HTTPException(status_code=404, detail="Account with that ID does not exist")

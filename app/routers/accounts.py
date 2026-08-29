from fastapi import APIRouter, HTTPException
from app.core import common
from app.core.cache import FileCache
import os

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/accounts.aof"))
router = APIRouter()

accounts = common.load_file(PATH, "aof")
last_change = common.file_last_change(PATH)
accounts_cache = FileCache(PATH, accounts, "aof", last_change)

@router.get('/accounts/{discord_id}', tags=['accounts'])
def get_account(discord_id: int) -> dict[str, str | int]:
    accounts_cache.check()

    if discord_id in accounts_cache.data:
        return {
                "PlayerUUID": accounts_cache.data[discord_id],
                "DiscordID": discord_id
                }
    else:
        raise HTTPException(status_code=404, detail="Account with that ID does not exist")

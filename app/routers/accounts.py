from fastapi import APIRouter, HTTPException
from app.core import common
import os

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/accounts.aof"))
router = APIRouter()

def load_accounts():
    f_json = {}
    try:
        with open(PATH, mode='r', encoding='utf-8-sig') as f:
            for line in f:
                word = line.split()
                if len(word) < 2:
                    continue
                f_json[int(word[0])] = word[1]
            return f_json
    except (FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail="File accounts.aof is unreachable")

accounts = load_accounts()
last_change = common.file_last_change(PATH)
@router.get('/accounts/{discord_id}', tags=['accounts'])
def get_account(discord_id: int):
    global accounts, last_change
    current_change = common.file_last_change(PATH)

    if current_change != last_change:
        last_change = current_change
        accounts = load_accounts()

    if discord_id in accounts:
        return accounts[discord_id]
    else:
        raise HTTPException(status_code=404, detail="Account with that ID does not exist")

from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get('/accounts/{discord_id}', tags=['accounts'])
def get_account(discord_id: int):
    try:
        with open("app/data/accounts.aof", mode='r', encoding='utf-8-sig') as accounts:
            for line in accounts:
                word = line.split()
                if len(word) < 2:
                    continue
                if str(discord_id) == word[0]:
                   return {"DiscordID": int(word[0]), "PlayerUUID": str(word[1])}
            raise HTTPException(status_code=404, detail="Account with that ID does not exist")
    except (FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail="File accounts is unreachable")
from fastapi import APIRouter

router = APIRouter()

@router.get('/accounts/{discord_id}', tags=['accounts'])
def get_account(discord_id: int):
    with open("data/accounts.aof", mode='r', encoding='utf-8-sig') as accounts:
        for line in accounts:
            word = line.split()
            if str(discord_id) == word[0]:
                return {"DiscordID": int(word[0]),
                        "PlayerUUID": str(word[1])}

        return {"Error": "Account with that ID does not exist"}
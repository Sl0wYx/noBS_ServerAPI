from fastapi import APIRouter, Request, HTTPException
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi.responses import FileResponse

load_dotenv(Path("app/data/private/.env"))

IMAGE_URL = "https://api.noboobs.world/get_image"
API_TOKEN = os.getenv("API_TOKEN")
router = APIRouter()

@router.get("/get_image/{date}", tags=["telegram"])
async def get_image(date : str):
    date_str = str(date.replace(" ", "_").replace(":", "-"))
    local_url = Path(f"/home/noboobs/noBS_BotIntegrator/src/{date_str}.png")
    return FileResponse(local_url)

@router.get("/get_message", tags=["telegram"])
async def get_message():
    with open("app/data/message.json", mode='r', encoding='utf-8-sig') as message:
            return json.load(message)

@router.post('/receive_message', tags=["telegram"])
async def receive_message(data: dict, request: Request):
    if request.headers.get("authorization") != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API Token")
    else:
        base = Path("app/data")
        path = base / "message.json"

        date_str = str(data.get("date")).replace(" ", "_").replace(":", "-")
        if data.get("image"):
            image_dict = {"image" : f"{IMAGE_URL}/{date_str}"}
            data.update(image_dict)
        
        path.write_text(json.dumps(data))
        
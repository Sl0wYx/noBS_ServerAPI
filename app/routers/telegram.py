from fastapi import APIRouter, Request, HTTPException
from app.core import common
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from fastapi.responses import FileResponse

MSG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/message.json"))
IMG_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/images/"))
IMG_FOLDER_REAL_PATH = os.path.realpath(IMG_FOLDER_PATH)
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/private/.env"))
load_dotenv(ENV_PATH)

API_TOKEN = os.getenv("API_TOKEN")
API_URL = os.getenv("API_URL")
IMAGE_URL = "https://api.noboobs.world/get_image"
router = APIRouter()

ALLOWED_CHARS = set("123467890-_")
@router.get("/get_image/{date}", tags=["telegram"])
def get_image(date : str):
    date_str = str(date.replace(" ", "_").replace(":", "-"))
    local_url = Path(os.path.join(IMG_FOLDER_PATH, f"{date_str}.png"))

    if not set(date_str) <= ALLOWED_CHARS:
        raise HTTPException(status_code=400, detail="Invalid characters!")

    dir_name = os.path.dirname(os.path.realpath(local_url))
    if dir_name != IMG_FOLDER_REAL_PATH:
        raise HTTPException(status_code=400, detail="Invalid folder!")

    if not local_url.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(local_url)

@router.get("/get_message", tags=["telegram"])
def get_message():
    try:
        with open(MSG_PATH, mode='r', encoding='utf-8-sig') as message:
            return json.load(message)
    except (FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail="File message is unreachable")

@router.post('/receive_message', tags=["telegram"])
def receive_message(data: dict, request: Request):
    if request.headers.get("authorization") != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API Token")
    else:
        base = Path(os.path.join(os.path.dirname(__file__), "../data/"))
        path = base / "message.json"

        if not base.exists():
            raise HTTPException(status_code=404, detail=f"Path {base} not found")

        date_str = str(data.get("date")).replace(" ", "_").replace(":", "-")
        if data.get("image"):
            image_dict = {"image" : f"{IMAGE_URL}/{date_str}"}
            data.update(image_dict)

        try:
            path.write_text(json.dumps(data))
        except IOError:
            raise HTTPException(status_code=500, detail="Failed to write message")

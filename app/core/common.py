import os
from fastapi import HTTPException

def file_last_change(path):
    try:
        path = os.stat(path).st_mtime
        return path
    except (FileNotFoundError, IOError):
        raise HTTPException(status_code=500, detail="File accounts.aof is unreachable")
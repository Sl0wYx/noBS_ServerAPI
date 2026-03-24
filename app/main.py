from fastapi import Depends, FastAPI
from app.routers import accounts
from app.routers import stats
from app.routers import online
app = FastAPI()

app.include_router(accounts.router)
app.include_router(stats.router)
app.include_router(online.router)
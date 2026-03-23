from fastapi import Depends, FastAPI
from routers import accounts
from routers import stats
from routers import online
app = FastAPI()

app.include_router(accounts.router)
app.include_router(stats.router)
app.include_router(online.router)
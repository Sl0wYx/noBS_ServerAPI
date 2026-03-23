from fastapi import Depends, FastAPI
import accounts
import stats
import online
app = FastAPI()

app.include_router(accounts.router)
app.include_router(stats.router)
app.include_router(online.router)
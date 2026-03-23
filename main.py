from fastapi import Depends, FastAPI
import accounts
import stats
app = FastAPI()

app.include_router(accounts.router)
app.include_router(stats.router)

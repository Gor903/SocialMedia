from fastapi import FastAPI, status, HTTPException
from api.v1 import models

from api import router as api_v1_router
from core.database import engine
from api.v1.dependencies import (
    db_dependency,
    user_dependency,
)

app = FastAPI()
app.include_router(api_v1_router)

models.Base.metadata.create_all(bind=engine)


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"user": user}

import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn


sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as auth_router
from src.config import settings


app = FastAPI()

app.include_router(auth_router)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck():
    return {"healthcheck": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)

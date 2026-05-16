import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.config import get_settings
from app.database import init_db
from app.routes import api_router

settings = get_settings()
logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.upload_dir, exist_ok=True)
    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/errors")
def show_error(msg: str = ""):
    html = f"<html><body><h1>Error</h1><p>{msg}</p></body></html>"
    return HTMLResponse(content=html, status_code=200)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.getLogger("access").info("%s %s", request.method, str(request.url))
    response = await call_next(request)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.debug)

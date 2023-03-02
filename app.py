from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from engine.endpoints import router as engine_router
from settings import settings

app = FastAPI(title="Homestead Solar", root_path=settings.root_path)


async def startup_event():
    logger.info("solar startup")


async def shutdown_event():
    logger.info("solar shutdown")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
def hello_endpoint():
    return "hello"


@app.get("/settings")
def get_settings():
    return {"client_id": settings.client_id}


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

app.include_router(engine_router, prefix="/engine")

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from day.endpoints import router as day_router
from router import routers
from settings import settings

if dsn := settings.sentry_dsn:
    sentry_sdk.init(dsn=dsn, traces_sample_rate=1)

app = FastAPI(
    title="Homestead Solar",
    root_path=settings.root_path,
    root_path_in_servers=False,
    servers=[
        {"url": "/solar", "description": "solar"},
        {"url": "https://api.zumbrohomestead.com", "description": "main"},
    ],
)


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


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

for router in routers:
    app.include_router(router.router, prefix=router.prefix)

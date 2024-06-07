from fastapi import APIRouter, Request
from loguru import logger

router = APIRouter()


@router.get("/", response_model=str)
def get_request(request: Request):
    logger.info(request.__dict__)
    return "ok"

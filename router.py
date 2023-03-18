from dataclasses import dataclass

from fastapi import APIRouter

from day.endpoints import router as day_router


@dataclass
class Router:
    prefix: str
    router: APIRouter

    def __lt__(self, other):
        return self.prefix < other.prefix


routers = sorted((Router(router=day_router, prefix="/day"),))

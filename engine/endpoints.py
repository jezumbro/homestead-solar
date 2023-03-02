from client.enphase_client import EnPhaseClient, get_en_phase_client
from fastapi import APIRouter, Depends

from engine.dependencies import get_engine_repo
from engine.model import Engine
from engine.repository import EngineRepo
from engine.request_schema import CreateEngineRequest
from engine.response_schema import EngineResponse

router = APIRouter()


@router.post("", response_model=EngineResponse)
def create_engine(
    req: CreateEngineRequest,
    repo: EngineRepo = Depends(get_engine_repo),
    client: EnPhaseClient = Depends(get_en_phase_client),
):
    resp = client.get_token(req.code, req.redirect_uri)
    existing_engine = repo.find_one_by({"user_id": resp.enl_uid})
    engine = existing_engine or Engine(user_id=resp.enl_uid)
    engine.set_tokens(resp.dict())
    repo.save(engine)
    return engine

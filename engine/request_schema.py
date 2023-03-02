from pydantic import AnyHttpUrl, BaseModel


class CreateEngineRequest(BaseModel):
    code: str
    redirect_uri: AnyHttpUrl

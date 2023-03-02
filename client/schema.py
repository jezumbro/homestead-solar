from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    app_type: str
    enl_cid: str
    enl_password_last_changed: str
    expires_in: int
    is_internal_app: bool
    jti: str
    enl_uid: str
    expires_in: int
    is_internal_app: str
    refresh_token: str
    scope: str
    jti: str
    refresh_token: str
    token_type: str

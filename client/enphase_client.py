import base64
from typing import Optional

import requests
from settings import settings

from client.schema import TokenResponse


class EnPhaseClient:
    def __init__(
        self,
        *,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.base_url = base_url or "https://api.enphaseenergy.com"
        self.client_id = client_id or settings.client_id
        self.client_secret = client_secret or settings.client_secret

    def url(self, endpoint: str):
        assert endpoint.startswith("/"), "must lead with / for endpoints"
        return self.base_url + endpoint

    @property
    def header_code(self):
        return base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode("ascii")
        ).decode("ascii")

    def get_token(self, code: str, redirect_uri: str) -> TokenResponse:
        resp = requests.post(
            self.url("/oauth/token"),
            headers={"authorization": f"Basic {self.header_code}"},
            params={
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
                "code": code,
            },
        )
        return TokenResponse.parse_obj(resp.json())


def get_en_phase_client():
    return EnPhaseClient()

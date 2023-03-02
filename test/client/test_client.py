import pytest

from client.enphase_client import EnPhaseClient


@pytest.fixture
def en_phase_client():
    return EnPhaseClient(
        client_id="abcd", client_secret="uvwxyz", base_url="http://test"
    )


def test_invalid_endpoint_raises(en_phase_client):
    with pytest.raises(AssertionError):
        en_phase_client.url("foobar")


def test_correct_header_code(en_phase_client):
    assert en_phase_client.header_code == "YWJjZDp1dnd4eXo="

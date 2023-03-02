import pytest
from rsa_helper import decrypt, encrypt


@pytest.mark.parametrize("value", ("some random string", "a super long string" * 100))
def test_decrypt_and_encrypt(value):
    q = encrypt(value)
    assert isinstance(q, str)
    assert q != value, "should be encrypted"
    foo = decrypt(q)
    assert foo == value, "should match original"

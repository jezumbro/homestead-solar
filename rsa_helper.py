from typing import Optional

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from more_itertools import chunked

from settings import settings

if not settings.rsa_file:
    raise Exception(
        f"Cannot encrypt anything due to a file not found for rsa_file={settings.rsa_file}"
    )
public_key = RSA.importKey(
    open(str(settings.rsa_file).replace(".pem", ".pub"), "rb").read()
)
private_key = RSA.importKey(open(settings.rsa_file, "rb").read())

line_joiner = "\n\n\n"


def chunk_encrypt(value: str, cipher) -> bytes:
    for chunk in chunked(list(value), 20, False):
        yield cipher.encrypt("".join(chunk).encode()).hex()


def parse_decrypt(value: str, cipher) -> str:
    for encrypted in value.split(line_joiner):
        yield cipher.decrypt(bytearray.fromhex(encrypted)).decode()


def encrypt(value: str) -> str:
    cipher = PKCS1_OAEP.new(public_key)
    return line_joiner.join(chunk_encrypt(value, cipher))


def decrypt(value: Optional[str]) -> str:
    cipher = PKCS1_OAEP.new(private_key)
    if not value:
        return value
    message = "".join(parse_decrypt(value, cipher))
    return message

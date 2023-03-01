from typing import Union


def parse_csv(string: Union[str, list[str]]) -> list[str]:
    if isinstance(string, list):
        return string
    return string.split(",")

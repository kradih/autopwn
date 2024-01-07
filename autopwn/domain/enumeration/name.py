from enum import Enum


class NameStatus(Enum):
    UP = 1
    DOWN = 2
    UNKNOWN = 3


class Name:
    def __init__(self, fqdn: str, status: NameStatus) -> None:
        self.fqdn = fqdn
        self.status = status

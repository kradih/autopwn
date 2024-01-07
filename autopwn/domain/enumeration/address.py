from enum import Enum


class AddressFamily(Enum):
    INET4 = 1
    INET6 = 2


class AddressStatus(Enum):
    UP = 1
    DOWN = 2
    UNKNOWN = 3


class Address:
    def __init__(
        self, address: str, family: AddressFamily, status: AddressStatus
    ):
        self.address = address
        self.family = family
        self.status = status

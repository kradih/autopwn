from typing import List

from .address import Address
from .name import Name


class Host:
    def __init__(self, names: List[Name], addresses: List[Address]) -> None:
        self.names = names
        self.addresses = addresses

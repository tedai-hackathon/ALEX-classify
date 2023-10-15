"""
"""

from typing import List
from ..flag import Flag


class Entity:
    """ """

    _mnemonic: str
    _name: str
    _state: str
    _statue: str
    _docs: str
    _description: str
    _flags: List[Flag]

    def __init__(
        self,
        mnemonic: str,
        name: str,
        state: str,
        statue: str,
        docs: str,
        description: str,
        flags: List[Flag],
    ):
        self._mnemonic = mnemonic
        self._name = name
        self._state = state
        self._statue = statue
        self._docs = docs
        self._description = description
        self._flags = flags

    @property
    def mnemonic(self) -> str:
        return self._mnemonic

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> str:
        return self._state

    @property
    def statue(self) -> str:
        return self._statue

    @property
    def docs(self) -> str:
        return self._docs

    @property
    def description(self) -> str:
        return self._description

    @property
    def flags(self) -> List[Flag]:
        return self._flags

    @flags.setter
    def flags(self, flags: List[Flag]):
        self._flags = flags

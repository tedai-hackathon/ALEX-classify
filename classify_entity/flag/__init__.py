"""
"""
from typing import List


class Flag:
    """ """

    _mnemonic: str
    _name: str
    _description: str
    _question: str
    _deps: List[str]

    def __init__(
        self, mnemonic: str, name: str, description: str, question: str, deps: List[str]
    ):
        self._mnemonic = mnemonic
        self._name = name
        self._description = description
        self._question = question
        self._deps = deps

    @property
    def mnemonic(self) -> str:
        return self._mnemonic

    @property
    def name(self) -> str:
        return self._name

    @property
    def question(self) -> str:
        return self._question

    @property
    def deps(self) -> List[str]:
        return self._deps

    @property
    def description(self) -> str:
        return self._description

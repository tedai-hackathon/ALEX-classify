"""
"""


class Flag:
    """ """

    _mnemonic: str
    _name: str
    _description: str

    def __init__(self, mnemonic: str, name: str, description: str):
        self._mnemonic = mnemonic
        self._name = name
        self._description = description

    @property
    def mnemonic(self) -> str:
        return self._mnemonic

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

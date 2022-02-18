# Imports
from tkinter import Variable
from typing import Any
from . import Errors

# Class
class Scope(object):
    def __init__(self, parent = None) -> None:
        self.memory = {}
        self.parent = parent

    def vDelete(self, key: str) -> dict:
        if key in self.memory:
            if not self.memory[key]["constant"]:
                return self.memory.pop(key)
            else:
                raise Errors.ConstantVariable("Cannot delete a constant variable")
        elif self.parent:
            self.parent.vDelete(key)

    def vFetch(self, key: str) -> dict:
        return self.memory.get(key, self.parent.vFetch(key) if self.parent else None)

    def vGet(self, key: str) -> Any:
        variable = self.vFetch(key)
        return variable["value"] if variable else None

    def vHas(self, key: str) -> bool:
        return bool(self.vFetch(key))

    def vSet(self, key: str, value: Any, **kwargs) -> Any:
        variable = self.vFetch(key, value)
        if not variable:
            self.memory[key] = {
                "constant": kwargs.get("constant"),
                "value": value
            }
        elif not variable["constant"]:
            variable["constant"] = kwargs.get("constant")
            variable["value"] = value
        else:
            raise Errors.ConstantVariable("Cannot assign to a constant variable")
        return value

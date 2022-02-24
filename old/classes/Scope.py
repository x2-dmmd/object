# Imports
from classes import Exceptions
from typing import Any

# Class
class Scope:
    def __init__(self, interpreter, parent = None) -> None:
        self.interpreter = interpreter
        self.parent = parent
        self.variables = {}
    
    def vClear(self, force: bool = False, wipe: bool = False) -> None:
        if force:
            self.variables = {}
        else:
            for key in list(self.variables.keys()):
                if not self.variables[key]["constant"]:
                    self.vDelete(key)
        if wipe and self.parent:
            self.parent.vClear(self, force, wipe)

    def vDelete(self, key: str) -> dict | None:
        if key in self.variables and self.variables[key]["constant"]:
            raise Exceptions.ConstantDelete("Cannot delete a constant variable")
        return self.variables.pop(key) if key in self.variables else self.parent.vDelete(key) if self.parent else None

    def vFetch(self, key: str) -> dict | None:
        return self.variables.get(key, self.parent.vFetch(key) if self.parent else None)

    def vGet(self, key: str, default: Any = None) -> Any:
        fetched = self.vFetch(key)
        return fetched["value"] if fetched else default

    def vHas(self, key: str) -> bool:
        return bool(self.vFetch(key))

    def vSet(self, key: str, value: Any = None, constant: bool = False, force: bool = False) -> Any:
        fetched = self.vFetch(key)
        data = {
            "constant": constant,
            "value": value
        }
        if not fetched:
            self.variables[key] = data
        else:
            if force:
                local = self.variables.get(key, None)
                if local:
                    if local["constant"]:
                        raise Exceptions.ConstantAssignment("Cannot assign value to a constant variable")
                    else:
                        self.variables[key] = data
            else:
                if fetched["constant"]:
                    raise Exceptions.ConstantAssignment("Cannot assign value to a constant variable")
                for dKey, dValue in data.items():
                    fetched[dKey] = dValue
        return value

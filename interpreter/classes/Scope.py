# Imports
import os
from . import Exceptions

# Class
class Scope(object):
    def __init__(self, parent, file):
        self.memory = {}
        self.parent = parent
        self.file = file

    def vDelete(self, key):
        if key in self.memory[key]:
            if self.memory[key]["constant"]:
                raise Exceptions.ConstantVariableException(f"Cannot delete a value of a constant variable <{key}>")
            return self.memory.pop(key) if key in self.memory else None
        elif self.parent:
            self.parent.vDelete(key)
        else:
            return None

    def vFetch(self, key):
        return self.memory[key] if key in self.memory else self.parent.vFetch(key) if self.parent else None

    def vGet(self, key, default = None):
        variable = self.vFetch(key)
        return variable["value"] if variable else default

    def vHas(self, key):
        return bool(self.vFetch(key))

    def vSet(self, key, value, **kwargs):
        variable = self.vFetch(key)
        data = {
            "constant": bool(kwargs.get("constant")),
            "section": bool(kwargs.get("section")),
            "scope": kwargs.get("scope"),
            "value": value
        }
        if not variable:
            self.memory[key] = data
        elif not variable["constant"]:
            for key, value in data.items():
                variable[key] = value
        else:
            raise Exceptions.ConstantVariableException(f"Cannot change a value of a constant variable <{key}>")
        return value

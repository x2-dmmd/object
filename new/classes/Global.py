# Imports
import os
import sys
from . import Errors
from .Scope import Scope

class Global(Scope):
    def __init__(self) -> None:
        Scope.__init__(self, None)
        self.modules = {}

    def group(self, code):
        stacks = []
        group = stacks
        for line in code.split("\n"):
            line = line.strip()
            if not line or line.startswith("::"):
                continue
            if line.startswith((":", "if")):
                new = []
                group.append(new)
                stacks.append(group)
                group = new
            group.append(line)
            if line.startswith("end"):
                group = stacks.pop()
                if not isinstance(group, list):
                    raise Errors.InvalidStack("Invalid stack (did you put an extra 'end' operator)")
        return stacks

    def load(self, path):
        if not os.path.isfile(path):
            raise Errors.FileNotFound(f"Cannot load module '{path}'")
        absPath = os.path.abspath(path)
        if absPath not in self.modules:
            self.modules[absPath] = {}
            with open(absPath, "r") as file:
                groups = self.group(file.read())
                print(groups)
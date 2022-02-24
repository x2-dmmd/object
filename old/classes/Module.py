# Imports
import os
from classes import Exceptions
from classes.Field import Field
from classes.Scope import Scope
from functions import parser

# Class
class Module:
    def __init__(self, path: str, interpreter) -> None:
        self.exports = {}
        self.interpreter = interpreter
        self.path = os.path.abspath(path).replace("\\", "/")
        self.field = None
        if not self.path.endswith(".obx2"):
            self.path += ".obx2"

    def run(self) -> None:
        if not os.path.isfile(self.path):
            raise Exceptions.ModuleNotFound(f"Cannot find module '{self.path}'")
        if self.interpreter.oHas(self.path):
            raise Exceptions.ModuleConflict(f"Module '{self.path}' already exists")
        self.field = Field(parser.parseFile(self.path), self, Scope(self.interpreter, self.interpreter))
        self.field.run()
        if self.field.broke:
            raise Exceptions.ModuleBreak("Cannot use 'brk' in the module scope")
        if self.field.returned:
            raise Exceptions.ModuleReturn("Cannot use 'ret' in the module scope")
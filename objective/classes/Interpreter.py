# Imports
from classes import Exceptions
from classes.Module import Module
from classes.Scope import Scope
from functions import parser
from types import FunctionType
from typing import Any

# Class
class Interpreter(Scope):
    def __init__(self, build: dict, config: dict) -> None:
        super().__init__(self, None)
        self.build = build
        self.config = config
        self.operators = {}
        self.modules = {}

    def executeLine(self, line: str, module: Module, scope: Scope) -> Any:
        operator, args = parser.parseLine(line, module, scope)
        if not self.oHas(operator):
            raise Exceptions.OperatorNotFound(f"Cannot find operator {operator}")
        return self.oGet(operator)(self, module, scope, args)

    def oDelete(self, key: str) -> FunctionType | None:
        return self.operators.pop(key) if key in self.operators else None
    
    def oGet(self, key: str) -> FunctionType | None:
        return self.operators.get(key, None)
    
    def oHas(self, key: str) -> bool:
        return key in self.operators
    
    def oSet(self, key: str, value: FunctionType) -> FunctionType:
        self.operators[key] = value
        return value
    
    def mDelete(self, key: str) -> dict | None:
        return self.modules.pop(key) if key in self.modules else None
    
    def mGet(self, key: str) -> dict | None:
        return self.modules.get(key, None)
    
    def mHas(self, key: str) -> bool:
        return key in self.modules
    
    def mImport(self, path: str) -> Module:
        if self.mHas(path):
            raise Exceptions.ModuleConflict(f"Module '{path}' already exist")
        module = Module(path, self)
        self.mSet(module.path, module)
        module.run()
    
    def mSet(self, key: str, value: dict) -> dict:
        self.modules[key] = value
        return value

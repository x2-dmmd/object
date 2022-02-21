# Imports
from classes.Scope import Scope

# Class
class Section(Scope):
    def __init__(self, module, scope: Scope, fields: list) -> None:
        super().__init__(module.interpreter, scope)
        self.name, *self.args = fields[0].split(" ")[1:]
        self.fields = fields[1:]
        self.interpreter = module.interpreter
        self.module = module

    def __repr__(self) -> None:
        return f"[section {self.name}]"
# Imports
from classes import Exceptions
from classes.Scope import Scope
from functions import tools

# Class
class Section:
    def __init__(self, module, scope: Scope, declarer: str, field) -> None:
        self.name, *self.args = declarer.split(" ")[1:]
        for arg in self.args:
            if not arg[0].isalpha() or any([character not in tools.characters for character in arg]):
                raise Exceptions.BadToken(f"Unexpected token '{arg}'")
        self.field = field
        self.interpreter = module.interpreter
        self.module = module
        self.scope = scope

    def __repr__(self) -> None:
        return f"[section {self.name}]"

    def run(self):
        value = self.field.run()
        if self.field.broke:
            raise Exceptions.SectionBreak("Cannot use 'brk' in the section scope")
        if self.field.returned:
            return value

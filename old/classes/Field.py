# Imports
from classes import Exceptions
from classes.Section import Section
from classes.Scope import Scope

# Class
class Field(Scope):
    def __init__(self, fields: list, module, scope: Scope) -> None:
        super().__init__(module.interpreter, scope)
        self.broke = False
        self.fields = fields
        self.module = module
        self.returned = False
    
    def run(self) -> None:
        for field in self.fields:
            if isinstance(field, list) and field[0].startswith("sect "):
                section = Section(self.module, self, field[0], Field(field[1:], self.module, self))
                self.vSet(section.name, section)
        for field in self.fields:
            if isinstance(field, list):
                if field[0].startswith("if "):
                    branches = []
                    branch = []
                    last = False
                    for line in field:
                        if isinstance(line, str) and (line.startswith("else if ") or line == "else"):
                            if last:
                                raise Exceptions.BranchOverflow("Cannot have an 'else if' branch after the 'else' branch")
                            last = line == "else"
                            branches.append(branch)
                            branch = []
                        branch.append(line)
                    if branch:
                        branches.append(branch)
                    for branch in branches:
                        subfield = Field(branch[1:], self.module, self)
                        selected = False
                        selected = selected or (branch[0].startswith("if ") and self.interpreter.executeLine(branch[0], self.module, subfield))
                        selected = selected or (branch[0].startswith("else if ") and self.interpreter.executeLine(branch[0][5:], self.module, subfield))
                        selected = selected or (branch[0] == "else")
                        if selected:
                            value = subfield.run()
                            if subfield.broke:
                                self.broke = True
                                return
                            if subfield.returned:
                                self.returned = True
                                return value
                            break
                elif field[0].startswith(("repeat ", "while ")):
                    subfield = Field(field[1:], self.module, self)
                    value = self.interpreter.executeLine(field[0], self.module, subfield)
                    if subfield.returned:
                        self.returned = True
                        return value
                elif field[0] == "try":
                    print(field)
            else:
                value = self.interpreter.executeLine(field, self.module, self)
                if self.broke:
                    return
                if self.returned:
                    return value
    

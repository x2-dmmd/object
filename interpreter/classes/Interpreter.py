# Imports
import os
import re
from . import Exceptions
from .Scope import Scope
from ..source import tools
from types import NoneType

# Variables
constants = [
    [ "true", True ],
    [ "false", False ],
    [ "null", None ],
    [ "Null", NoneType ],
    [ "array", list ],
    [ "object", dict ],
    [ "string", str ],
    [ "number", float ],
    [ "bool", bool ],
    [ "stringEmpty", "" ]
]
wrappers = {
    "double": [ "\"", "\"" ],
    "single": [ "'", "'" ],
    "group": [ "(", ")" ] 
}

# Class
class Interpreter(Scope):
    def __init__(self, build, config):
        Scope.__init__(self, None, None)
        self.build = build
        self.config = config
        self.modules = {}
        self.operators = {}
        self.scope = self
        self.stack = []
        for key, value in constants:
            self.vSet(key, value, constant = True)
    
    def execute(self, line, scope):
        operator, arguments = self.parseLine(line, scope)
        for i in range(len(arguments)):
            if not arguments[i]:
                continue
            if arguments[i][0] == "(":
                arguments[i] = self.execute(arguments[i][1:-1], scope)
            if arguments[i][0] in [ "\"", "'" ]:
                while "$(" in arguments[i] and ")" in arguments[i]:
                    string = arguments[i]
                    start = string.rindex("$(")
                    end = re.search(r"(?<!\\)\)", string[start:]).start() + start
                    executable = string[start + 2:end].encode("latin1").decode("unicode_escape")
                    arguments[i] = string[0:start] + str(self.execute(executable, scope = scope)) + string[end + 1:]
        return self.oGet(operator)(self, [ self.parseArgument(argument, scope) for argument in arguments ], line, scope) or "null"

    def oDelete(self, key):
        return self.operators.pop(key) if key in self.operators else None

    def oGet(self, key, default = None):
        return self.operators.get(key, default)

    def oHas(self, key):
        return key in self.operators

    def oSet(self, key, function):
        self.operators[key] = function

    def loop(self, lines, scope):
        for line in lines:
            if isinstance(line, str):
                self.execute(line, scope)
            elif isinstance(line, list):
                if not line[0].startswith(":"):
                    self.stack.append(scope)
                    self.scope = Scope(scope, scope.file)
                    if line[0].startswith("if"):
                        run = False
                        for subline in line[:-1]:
                            if run and subline.startswith(("else if", "else", "end")):
                                self.execute("end", self.scope)
                                break
                            if run:
                                self.execute(subline, self.scope)
                            if not run:
                                if subline.startswith("if") and self.execute(subline, self.scope) == True:
                                    run = True
                                elif subline.startswith("else if") and self.execute(subline[5:], self.scope) == True:
                                    run = True
                                    pass
                                elif subline.startswith("else") and not subline.startswith("else if"):
                                    run = True

    def parseArgument(self, argument, scope):
        data = {
            "constant": False,
            "section": False,
            "raw": argument,
            "scope": scope
        }
        if argument and (argument[0] == "\"" or argument[0] == "'"):
            data["type"] = "string"
            data["value"] = argument[1:-1].encode("latin1").decode("unicode_escape")
        elif argument and tools.isNumber(argument):
            data["type"] = "number"
            data["value"] = argument
        else:
            if not scope.vHas(argument):
                scope.vSet(argument, None, scope = scope)
            variable = scope.vFetch(argument)
            data["constant"] = variable["constant"]
            data["section"] = variable["section"]
            data["scope"] = variable["scope"]
            data["value"] = variable["value"]
            if isinstance(data["value"], str) and (data["value"][0] == "\"" or data["value"][0] == "'"):
                data["type"] = "string"
                data["value"] = data["value"][1:-1].encode("latin1").decode("unicode_escape")
            elif tools.isNumber(data["value"]):
                data["type"] = "number"
                data["value"] = data["value"]
            elif isinstance(variable["value"], bool):
                data["type"] = "boolean"
            elif variable["value"] == None:
                data["type"] = "null"
            elif type(variable["value"]) == type:
                data["type"] = "class"
            elif variable["section"]:
                data["type"] = "section"
            else:
                data["type"] = type(data["value"])
        return data

    def parseLine(self, line, scope):
        words = line.split(" ")
        operator = words[0]
        if not self.oHas(operator):
            raise Exceptions.UnknownOperatorException("Unknown operator", line = line, file = scope.file, highlight = operator)
        arguments, mode, segments = [], None, []
        for word in words[1:]:
            segments.append(word)
            if word.startswith("::"):
                break
            if not mode:
                for key, value in wrappers.items():
                    if word and word[0] == value[0]:
                        mode = key
                        break
            if mode:
                joined = " ".join(segments)
                if len(joined) == 1:
                    raise Exceptions.InvalidSyntaxException("Unexpected token", line = line, file = scope.file, highlight = joined)
                if joined[-1] == wrappers[mode][1] and joined[-2] != "\\":
                    arguments.append(joined)
                    mode = None
                    segments = []
            else:
                arguments.append(segments[0])
                segments = []
        if mode:
            raise Exceptions.InvalidSyntaxException("Unclosed wrapper", line = line, file = scope.file, highlight = " ".join(segments))
        return [ operator, arguments ]
    
    def parseLines(self, code):
        lines = []
        stack = []
        current = lines
        for line in code.split("\n"):
            line = line.strip()
            if not line or line.startswith("::"):
                continue
            if line.startswith(( ":", "if", "for", "while" )):
                new = []
                stack.append(current)
                current.append(new)
                current = new
            current.append(line)
            if line.startswith("end"):
                current = stack.pop()
        return lines

    def parseScope(self, lines, scope):
        for line in lines:
            if isinstance(line, list):
                name = line[0].split(" ")[0][1:]
                if not name:
                    raise Exceptions.InvalidSectionException("Section names may not be empty", line = line[0], file = scope.file)
                if not tools.isValidName(name):
                    raise Exceptions.InvalidSectionException("Section name contains illegal characters or is invalid", line = line[0], file = scope.file, highlight = name)
                sectionScope = Scope(scope, scope.file)
                scope.vSet(name, line, section = True, scope = sectionScope)
                self.parseScope(line, sectionScope)

    def run(self, path):
        absolute = os.path.abspath(path)
        self.scope = Scope(self, absolute)
        self.modules[absolute] = {}
        with open(absolute, "r") as file:
            code = file.read()
        lines = self.parseLines(code)
        self.parseScope(lines, self.scope)
        self.loop(lines, self.scope)

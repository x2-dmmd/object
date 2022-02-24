# Imports
import json
import os
import re
import time
from classes import Exceptions
from types import FunctionType
from typing import Any

# Class
class Scope(object):
    def __init__(self, interpreter, parent = None, sections: list[list | str] = []) -> None:
        self.exception = None
        self.flags = set()
        self.interpreter = interpreter
        self.parent = parent
        self.sections = sections
        self.value = None
        self.variables = {}

    def flgAdd(self, flag: Any) -> Any:
        self.flags.add(flag)
        return flag

    def flgHas(self, flag: Any) -> None:
        return flag in self.flags

    def flgRemove(self, flag: Any) -> Any:
        if flag not in self.flags:
            return None
        self.flags.discard(flag)
        return flag

    def varClear(self, force: bool = False, local: bool = False) -> None:
        if force:
            self.variables = {}
        else:
            for key in self.variables:
                if not self.variables[key]["constant"]:
                    del self.variables[key]
        if not local and self.parent:
            self.parent.varClear(force, local)
    
    def varDelete(self, key: str, force: bool = False, local: bool = False) -> Any:
        if force and key in self.variables:
            return self.variables.pop(key)
        elif not force and key in self.variables:
            if self.variables[key]["constant"]:
                raise Exceptions.ConstantDelete(f"Cannot delete a constant variable", variable = key)
            return self.variables.pop(key)
        if not local and self.parent:
            return self.parent.varDelete(key, force, local)
    
    def varFetch(self, key: str, local: bool = False) -> dict | None:
        if key in self.variables:
            return self.variables[key]
        if not local and self.parent:
            return self.parent.varFetch(key, local)

    def varHas(self, key: str, local: bool = False) -> bool:
        return bool(self.varFetch(key, local))

    def varGet(self, key: str, local: bool = False, default: Any = None) -> Any:
        variable = self.varFetch(key, local)
        return variable["value"] if variable else default
    
    def varSet(self, key: str, value: Any, constant: bool = False, force: bool = False, local: bool = False):
        variable = self.varFetch(key, local)
        data = {
            "constant": constant,
            "value": value
        }
        if not variable or force:
            self.variables[key] = data
        elif variable:
            if variable["constant"]:
                raise Exceptions.ConstantSet(f"Cannot reassign to a constant variable", variable = key)
            for dKey, dValue in data.items():
                variable[dKey] = dValue
        return value

class Module(object):
    def __init__(self, interpreter, path: str) -> None:
        if not path.endswith(".obx2"):
            path += ".obx2"
        if not os.path.isfile(path):
            raise Exceptions.ModuleNotFound(f"Cannot find module '{path}'", path = path)
        self.exports = {}
        self.interpreter = interpreter
        self.path = os.path.abspath(path)
        with open(self.path, "r") as file:
            self.scope = Scope(interpreter, interpreter.globalScope, interpreter.parseSections(file.read()))

    def load(self) -> dict:
        if self.path in self.interpreter.modules:
            return self.exports
        self.interpreter.modules[self.path] = self
        self.interpreter.executeScope(self, self.scope)
        if self.scope.exception:
            exception = self.scope.exception
            raise exception if isinstance(exception, Exception) else Exceptions.InterpreterException(str(exception))
        if self.scope.flgHas("break"):
            raise Exceptions.ModuleOperatorBreak(f"Cannot use operator 'brk' in the module scope")
        if self.scope.flgHas("return"):
            raise Exceptions.ModuleOperatorReturn(f"Cannot use operator 'ret' in the module scope")
        return self.exports

    def reload(self) -> dict:
        self.unload()
        return self.load()

    def unload(self) -> None:
        if self.path not in self.interpreter.modules:
            raise Exceptions.ModuleNotLoaded(f"Module '{self.path} is not loaded", path = self.path)
        del self.interpreter.modules[self.path]
        self.exports = {}
        self.scope = Scope(self.interpreter, self.interpreter.globalScope)
    
class Register(object):
    def __init__(self, interpreter) -> None:
        self.interpreter = interpreter

    def registerCommand(self, names: list[str], function: FunctionType) -> FunctionType:
        for name in names:
            self.interpreter.commands[name] = function
        return function

    def registerOperator(self, name: str, function: FunctionType, first: bool = False, raw: bool = False, section: bool = False) -> dict:
        data = {
            "first": first,
            "function": function,
            "raw": raw,
            "section": section
        }
        self.interpreter.operators[name] = data

    def registerModule(self, path: str) -> Module:
        module = Module(self.interpreter, path)
        module.load()
        return module

    def unregisterCommand(self, name: str) -> FunctionType | None:
        return self.interpreter.commands.pop(name) if name in self.interpreter.commands else None

    def unregisterOperator(self, name: str) -> dict | None:
        return self.interpreter.operators.pop(name) if name in self.interpreter.operators else None

    def unregisterModule(self, path: str) -> Module | None:
        abspath = os.path.abspath(path)
        if abspath not in self.interpreter.modules:
            return None
        module = self.interpreter.modules[abspath]
        module.unload()
        return module

class Interpreter(object):
    def __init__(self) -> None:
        self.path = os.path.normpath(os.path.join(__file__, "../../"))
        with open(os.path.join(self.path, "src/build.json"), "r") as file:
            self.build = json.loads(file.read())
        if os.path.isfile(".obx2config"):
            with open(".obx2config", "r") as file:
                self.config = json.loads(file.read())
        else:
            self.config = {}
        self.commands = {}
        self.globalScope = Scope(self)
        self.modules = {}
        self.operators = {}
        self.register = Register(self)
        self.startTime = round(time.time() * 1000, 7)

    def executeCommand(self, command: list, *args, **kwargs) -> Any:
        if not command[0] in self.commands:
            raise Exceptions.CommandNotFound(f"Command '{command[0]}' not found", command = " ".join(command))
        return self.commands[command[0]](self, command, *args, **kwargs)

    def executeScope(self, module: Module, scope: Scope) -> Any:
        for section in scope.sections:
            line = section[0] if isinstance(section, list) else section
            if any([line.startswith(operator + " ") or line == operator for operator in self.operators.keys() if self.operators[operator]["first"]]):
                operator, args = self.parseTokens(module, scope, line)
                self.operators[operator]["function"](self, module, scope, section, args)
                if scope.exception or scope.flgHas("break"):
                    break
                if scope.flgHas("return"):
                    return scope.value
        for section in scope.sections:
            line = section[0] if isinstance(section, list) else section
            if any([line.startswith(operator + " ") or line == operator for operator in self.operators.keys() if not self.operators[operator]["first"]]):
                operator, args = self.parseTokens(module, scope, line)
                self.operators[operator]["function"](self, module, scope, section, args)
                if scope.exception or scope.flgHas("break"):
                    break
                if scope.flgHas("return"):
                    return scope.value

    def parseSections(self, content: str) -> list[list | str]:
        lines = []
        line = ""
        comment = False
        previous = ""
        string = None
        group = False
        for character in content:
            if character == "\n" and not string:
                if group:
                    raise Exceptions.TokenInvalid(f"Unclosed wrapper", line = line)
                if line.strip():
                    lines.append(line.strip())
                line = ""
                comment = False
                string = None
                group = False
            elif comment:
                if character == ":" and previous == ":":
                    comment = False
            elif string:
                if character == "\n" and previous == "\\":
                    line = line[:-2]
                else:
                    if ((character == "\"" and string == "double") or (character == "'" and string == "single")) and previous != "\\":
                        string = None
                    line += character
            elif (character == "\"" or character == "'") and not string and previous != "\\":
                string = {"\"": "double", "'": "single"}[character]
                line += character
            elif character in ["(", ")"] and previous != "\\":
                group = character == "("
                line += character
            elif character == ":" and previous == ":":
                comment = True
                line = line[:-2]
            elif not (character == " " and ("" if not line else line[-1]) == " " and not string):
                line += character
            previous = character
        if line.strip():
            if group or string:
                raise Exceptions.TokenInvalid(f"Unclosed wrapper", line = line)
            lines.append(line.strip())
        stack = []
        sections = []
        section = sections
        for line in lines:
            if line.split(" ")[0] not in self.operators:
                raise Exceptions.OperatorNotFound(f"Operator '{line.split(' ')[0]}' is not found", line = line)
            if any(line.startswith(operator + " ") or line == operator for operator in self.operators.keys() if self.operators[operator]["section"]):
                subsection = []
                section.append(subsection)
                stack.append(section)
                section = subsection
            if line.startswith("end ") or line == "end":
                if not stack:
                    raise Exceptions.SectionUnderflow(f"Cannot end the module section (Perhaps you placed an extra 'end' somewhere?)")
                section = stack.pop()
            else:
                section.append(line)
        if stack:
            raise Exceptions.SectionOverflow(f"Unclosed section (Perhaps you forgot to place an 'end' somewhere?)")
        return sections

    def parseTokens(self, module: Module, scope: Scope, line: str) -> list:
        tokens = []
        token = ""
        wrapper = None
        previous = ""
        for character in line:
            if character == " " and not wrapper:
                tokens.append(token)
                token = ""
                wrapper = None
                previous = ""
            elif character == "\"" and (wrapper == "double" or not wrapper) and previous != "\\":
                wrapper = None if wrapper else "double"
                token += character
            elif character == "'" and (wrapper == "single" or not wrapper) and previous != "\\":
                wrapper = None if wrapper else "single"
                token += character
            elif character == "(" and not wrapper and previous != "\\":
                wrapper = "group"
                token += character
            elif character == ")" and wrapper == "group" and previous != "\\":
                wrapper = None
                token += character
            else:
                token += character
        if token:
            tokens.append(token)
        for token in tokens:
            if not re.match(r"^(([+-]?((\d+\.?\d*)|(\d*\.\d+)))|(\(.*\))|(\".*\")|('.*')|([A-Za-z_][A-Za-z0-9_]*))$", token):
                raise Exceptions.TokenInvalid(f"Invalid token '{token}'", line = line)
        if tokens[0] not in self.operators:
            raise Exceptions.OperatorNotFound(f"Operator '{tokens[0]}' not found", line = line)
        operator = self.operators[tokens[0]]
        args = []
        for token in tokens[1:]:
            data = {
                "raw": token
            }
            if not operator["raw"]:
                if token.startswith(("\"", "'")):
                    data["value"] = token[1:-1]
                elif re.match(r"^[+-]?((\d+\.?\d*)|(\d*\.\d+))$", token):
                    parsed = float(token)
                    data["value"] = int(parsed) if parsed.is_integer() else parsed
                elif token.startswith("("):
                    parsed = self.parseTokens(module, scope, token[1:-1])
                    data["value"] = self.operators[parsed[0]]["function"](self, module, scope, token[1:-1], parsed[1])
                else:
                    data["value"] = scope.varGet(token)
            args.append(data)
        return [tokens[0], args]

    def exit(self) -> None:
        raise KeyboardInterrupt

    def python(self, code: str, **kwargs) -> None:
        eval(compile(code, "Objective x2 Python", mode = "exec"), {}, kwargs)

    @property
    def uptime(self):
        return round(time.time() * 1000, 7) - self.startTime

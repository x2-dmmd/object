# Imports
from classes import Exceptions
from classes.Scope import Scope
from classes.Section import Section
from classes.Module import Module
from types import NoneType
from typing import Any

# Functions
def oAdd(interpreter, module: Module, scope: Scope, args: list) -> float | int | str:
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'add' takes at least two arguments")
    if isinstance(args[0]["value"], str) or isinstance(args[0]["value"], str):
        args[0]["value"] = str(args[0]["value"])
        args[1]["value"] = str(args[1]["value"])
    return args[0]["value"] + args[1]["value"]

def oBrk(interpreter, module: Module, scope: Scope, args: list) -> None:
    scope.broke = True

def oCon(interpreter, module: Module, scope: Scope, args: list) -> Any:
    if not args:
        raise Exceptions.ArgumentMissing("Operator 'con' takes at least one argument")
    key = args[0]["raw"]
    if not key[0].isalpha():
        raise Exceptions.BadToken("Variable name must start with an alphabetical letter and can only contain alphabetical letters, digits, or underscopes")
    if len(args) == 1:
        return scope.vGet(key)
    else:
        return scope.vSet(key, args[1]["value"], True)

def oDel(interpreter, module: Module, scope: Scope, args: list) -> Any:
    if not args:
        raise Exceptions.ArgumentMissing("Operator 'del' takes at least one argument")
    key = args[0]["raw"]
    if not key[0].isalpha():
        raise Exceptions.BadToken("Variable name must start with an alphabetical letter and can only contain alphabetical letters, digits, or underscopes")
    return scope.vDelete(key)

def oDiv(interpreter, module: Module, scope: Scope, args: list) -> float | int:
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'div' takes at least two arguments")
    return args[0]["value"] / args[1]["value"]

def oEql(interpreter, module: Module, scope: Scope, args: list) -> bool:
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'eql' takes at least two arguments")
    return args[0]["value"] == args[1]["value"]

def oGeq(interpreter, module: Module, scope: Scope, args: list) -> bool:
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'geq' takes at least two arguments")
    return args[0]["value"] >= args[1]["value"]

def oGrt(interpreter, module: Module, scope: Scope, args: list) -> bool:
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'grt' takes at least two arguments")
    return args[0]["value"] > args[1]["value"]

def oIf(interpreter, module: Module, scope: Scope, args: list) -> bool:
    if not args:
        raise Exceptions.ArgumentMissing("Operator 'if' takes at least one argument")
    return bool(args[0]["value"])

def oJmp(interpreter, module: Module, scope: Scope, args: list) -> Any:
    if not args:
        raise Exceptions.ArgumentMissing("Operator 'jmp' takes at least one argument")
    if not isinstance(args[0]["value"], Section):
        raise Exceptions.ArgumentType("Operator 'jmp' takes an section", expected = "section", received = args[0]["value"].__class__.__name__)
    section = args[0]["value"]
    for i in range(min(len(args[1:]), len(section.args))):
        section.field.vSet(section.args[i], args[i + 1]["value"])
    section.field.vSet("arguments", [arg["value"] for arg in args[1:]], False, True)
    return args[0]["value"].run()

def oLeq(interpreter, module: Module, scope: Scope, args: list) -> bool:
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'leq' takes at least two arguments")
    return args[0]["value"] <= args[1]["value"]

def oMul(interpreter, module: Module, scope: Scope, args: list) -> bool:
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'mul' takes at least two arguments")
    return args[0]["value"] * args[1]["value"]

def oLes(interpreter, module: Module, scope: Scope, args: list) -> bool:
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'les' takes at least two arguments")
    return args[0]["value"] < args[1]["value"]

def oNeq(interpreter, module: Module, scope: Scope, args: list) -> bool:
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'neq' takes at least two arguments")
    return args[0]["value"] != args[1]["value"]

def oPrt(interpreter, module: Module, scope: Scope, args: list) -> None:
    values = []
    if interpreter.config.get("fancy") == True:
        for arg in args:
            value = arg["value"]
            code = None
            if isinstance(value, (bool, NoneType)):
                code = 93
                value = {True: "true", False: "false", None: "null"}.get(value)
            elif isinstance(value, (float, int)):
                code = 93
            elif isinstance(value, (type, Section)):
                code = 96
            values.append(str(value) if not code else f"\033[{code}m{str(value)}\033[0m")
    else:
        for arg in args:
            value = arg["value"]
            if isinstance(value, (bool, NoneType)):
                value = {True: "true", False: "false", None: "null"}.get(value)
            values.append(str(value))
    print(*[value for value in values])

def oRet(interpreter, module: Module, scope: Scope, args: list) -> Any:
    scope.returned = True
    if not args:
        return None
    return args[0]["value"]

def oRepeat(interpreter, module: Module, scope: Scope, args: list) -> Any:
    if not args:
        raise Exceptions.ArgumentMissing("Operator 'repeat' takes at least one arguments")
    if not isinstance(args[0]["value"], int):
        raise Exceptions.ArgumentType("Operator 'repeat' takes an integer", expected = "int", received = args[0]["value"].__class__.__name__)
    for i in range(args[0]["value"]):
        scope.vClear()
        value = scope.run()
        if scope.broke:
            break
        if scope.returned:
            return value

def oSub(interpreter, module: Module, scope: Scope, args: list) -> float | int:
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'sub' takes at least two arguments")
    return args[0]["value"] - args[1]["value"]

def oVar(interpreter, module: Module, scope: Scope, args: list) -> Any:
    if not args:
        raise Exceptions.ArgumentMissing("Operator 'var' takes at least one argument")
    key = args[0]["raw"]
    if not key[0].isalpha():
        raise Exceptions.BadToken("Variable name must start with an alphabetical letter and can only contain alphabetical letters, digits, or underscopes")
    if len(args) == 1:
        return scope.vGet(key)
    else:
        return scope.vSet(key, args[1]["value"])

def oWhile(interpreter, module: Module, scope: Scope, args: list) -> Any:
    if not args:
        raise Exceptions.ArgumentMissing("Operator 'while' takes at least one arguments")
    if not args[0]["raw"].startswith("("):
        raise Exceptions.ArgumentType("Operator 'while' takes a statement", expected = "statement", received = args[0]["value"].__class__.__name__)
    while args[0]["value"]:
        scope.vClear()
        value = scope.run()
        if scope.broke:
            break
        if scope.returned:
            return value
        args[0]["value"] = interpreter.executeLine(args[0]["raw"][1:-1], module, scope)

# Exports
operators = {
    "add": oAdd,
    "brk": oBrk,
    "con": oCon,
    "del": oDel,
    "div": oDiv,
    "eql": oEql,
    "geq": oGeq,
    "grt": oGrt,
    "if": oIf,
    "jmp": oJmp,
    "les": oLes,
    "leq": oLeq,
    "mul": oMul,
    "prt": oPrt,
    "repeat": oRepeat,
    "ret": oRet,
    "sub": oSub,
    "var": oVar,
    "while": oWhile
}
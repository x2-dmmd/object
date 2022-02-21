# Imports
from classes import Exceptions
from classes.Section import Section
from types import NoneType

# Functions
def oAdd(interpreter, module, scope, args):
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'add' takes at least two arguments")
    if isinstance(args[0]["value"], str) or isinstance(args[0]["value"], str):
        args[0]["value"] = str(args[0]["value"])
        args[1]["value"] = str(args[1]["value"])
    return args[0]["value"] + args[1]["value"]

def oBrk(interpreter, module, scope, args):
    scope.broke = True

def oDiv(interpreter, module, scope, args):
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'div' takes at least two arguments")
    return args[0]["value"] / args[1]["value"]

def oEql(interpreter, module, scope, args):
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'eql' takes at least two arguments")
    return args[0]["value"] == args[1]["value"]

def oGeq(interpreter, module, scope, args):
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'geq' takes at least two arguments")
    return args[0]["value"] >= args[1]["value"]

def oGrt(interpreter, module, scope, args):
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'grt' takes at least two arguments")
    return args[0]["value"] > args[1]["value"]

def oIf(interpreter, module, scope, args):
    if not args:
        raise Exceptions.ArgumentMissing("Operator 'if' takes at least one argument")
    return bool(args[0]["value"])

def oLeq(interpreter, module, scope, args):
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'leq' takes at least two arguments")
    return args[0]["value"] <= args[1]["value"]

def oMul(interpreter, module, scope, args):
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'mul' takes at least two arguments")
    return args[0]["value"] * args[1]["value"]

def oLes(interpreter, module, scope, args):
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'les' takes at least two arguments")
    return args[0]["value"] < args[1]["value"]

def oNeq(interpreter, module, scope, args):
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'neq' takes at least two arguments")
    return args[0]["value"] != args[1]["value"]

def oPrt(interpreter, module, scope, args):
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

def oRet(interpreter, module, scope, args):
    scope.returned = True
    if not args:
        return None
    return args[0]["value"]

def oRepeat(interpreter, module, scope, args):
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

def oSub(interpreter, module, scope, args):
    if len(args) < 2:
        raise Exceptions.ArgumentMissing("Operator 'sub' takes at least two arguments")
    return args[0]["value"] - args[1]["value"]

def oVar(interpreter, module, scope, args):
    if not args:
        raise Exceptions.ArgumentMissing("Operator 'var' takes at least one argument")
    key = args[0]["raw"]
    if not key[0].isalpha():
        raise Exceptions.BadToken("Variable name must start with an alphabetical letter and can only contain alphabetical letters, digits, or underscopes")
    if len(args) == 1:
        return scope.vGet(key)
    else:
        return scope.vSet(key, args[1]["value"])

def oWhile(interpreter, module, scope, args):
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
    "div": oDiv,
    "eql": oEql,
    "geq": oGeq,
    "grt": oGrt,
    "if": oIf,
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
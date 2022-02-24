# Imports
from classes import Exceptions
from classes.Components import Interpreter, Module, Scope
from types import FunctionType, NoneType
from typing import Any

# Functions
def operatorAdd(interpreter: Interpreter, module: Module, scope: Scope, section: list[list | str] | str, arguments: list[dict], *args, **kwargs) -> float | int | str:
    if len(arguments) < 2:
        raise Exceptions.ArgumentInvalid(f"Operator 'add' takes at least 2 arguments")
    a = arguments[0]["value"]
    b = arguments[1]["value"]
    return str(a) + str(b) if isinstance(a, str) or isinstance(b, str) else a + b

def operatorBrk(interpreter: Interpreter, module: Module, scope: Scope, section: list[list | str] | str, arguments: list[dict], *args, **kwargs) -> None:
    scope.flgAdd("break")

def operatorDiv(interpreter: Interpreter, module: Module, scope: Scope, section: list[list | str] | str, arguments: list[dict], *args, **kwargs) -> float | int | str:
    if len(arguments) < 2:
        raise Exceptions.ArgumentInvalid(f"Operator 'div' takes at least 2 arguments")
    return arguments[0]["value"] / arguments[1]["value"]

def operatorFunc(interpreter: Interpreter, module: Module, scope: Scope, section: list[list | str] | str, arguments: list[dict], *args, **kwargs) -> FunctionType:
    if not arguments:
        raise Exceptions.ArgumentInvalid(f"Operator 'func' takes at least 1 argument")
    def function(*args):
        subscope = Scope(interpreter, scope, section[1:])
        if len(arguments) > 1:
            for i in range(min(len(args), len(arguments) - 1)):
                subscope.varSet(arguments[i + 1]["raw"], args[i], False, True, True)
        subscope.varSet("arguments", list(args), False, True, True)
        interpreter.executeScope(module, subscope)
        if subscope.exception:
            scope.exception = subscope.exception
        if subscope.flgHas("break"):
            raise Exceptions.FunctionOperatorBreak(f"Cannot use operator 'brk' in the function scope")
        if subscope.flgHas("return"):
            scope.flgAdd("return")
            scope.value = subscope.value
            return subscope.value
    function.__name__ = arguments[0]["raw"]
    function.__qualname__ = ".".join([*function.__qualname__.split(".")[:-1], arguments[0]["raw"]])
    scope.varSet(arguments[0]["raw"], function)
    return function

def operatorJmp(interpreter: Interpreter, module: Module, scope: Scope, section: list[list | str] | str, arguments: list[dict], *args, **kwargs) -> Any:
    if not arguments:
        raise Exceptions.ArgumentInvalid(f"Operator 'jmp' takes at least 1 argument")
    if not isinstance(arguments[0]["value"], FunctionType):
        raise Exceptions.ArgumentInvalid(f"Operator 'jmp' takes a function as its first argument")
    value = arguments[0]["value"](*[argument["value"] for argument in arguments[1:]])

def operatorMod(interpreter: Interpreter, module: Module, scope: Scope, section: list[list | str] | str, arguments: list[dict], *args, **kwargs) -> float | int | str:
    if len(arguments) < 2:
        raise Exceptions.ArgumentInvalid(f"Operator 'mod' takes at least 2 arguments")
    return arguments[0]["value"] % arguments[1]["value"]

def operatorMul(interpreter: Interpreter, module: Module, scope: Scope, section: list[list | str] | str, arguments: list[dict], *args, **kwargs) -> float | int | str:
    if len(arguments) < 2:
        raise Exceptions.ArgumentInvalid(f"Operator 'mul' takes at least 2 arguments")
    return arguments[0]["value"] * arguments[1]["value"]

def operatorPrt(interpreter: Interpreter, module: Module, scope: Scope, section: list[list | str] | str, arguments: list[dict], *args, **kwargs) -> None:
    values = []
    if interpreter.config.get("fancy"):
        for value in arguments:
            if isinstance(value["value"], bool):
                values.append(f"\033[93m{'true' if value['value'] else 'false'}\033[0m")
            elif value["value"] == float("inf"):
                values.append(f"\033[93mInfinity\033[0m")
            elif value["value"] == -float("inf"):
                values.append(f"\033[93m-Infinity\033[0m")
            elif value["value"] == None:
                values.append("\033[93mnull\033[0m")
            elif value["value"] == bool:
                values.append(f"\033[96m[class Boolean]\033[0m")
            elif value["value"] == dict:
                values.append(f"\033[96m[class Object]\033[0m")
            elif value["value"] == Exception:
                values.append(f"\033[96m[class Error]\033[0m")
            elif value["value"] == float or value == int:
                values.append(f"\033[96m[class Number]\033[0m")
            elif value["value"] == FunctionType:
                values.append(f"\033[96m[class Function]\033[0m")
            elif value["value"] == list:
                values.append(f"\033[96m[class Array]\033[0m")
            elif value["value"] == NoneType:
                values.append("\033[93mNull\033[0m")
            elif value["value"] == object:
                values.append(f"\033[96m[class Attribute]\033[0m")
            elif value["value"] == set:
                values.append(f"\033[96m[class Set]\033[0m")
            elif value["value"] == str:
                values.append(f"\033[96m[class String]\033[0m")
            elif value["value"] == tuple:
                values.append(f"\033[96m[class Tuple]\033[0m")
            elif isinstance(value["value"], (float, int)):
                values.append(f"\033[93m{value['value']}\033[0m")
            elif isinstance(value["value"], FunctionType):
                values.append(f"\033[95m[function {value['value'].__name__}]\033[0m")
            elif isinstance(value["value"], type):
                values.append(f"\033[96m{repr(value['value'])}\033[0m")
            else:
                values.append(value['value'])
    else:
        for value in arguments:
            if isinstance(value["value"], bool):
                values.append("true" if value["value"] else "false")
            elif value["value"] == float("inf"):
                values.append("Infinity")
            elif value["value"] == -float("inf"):
                values.append("-Infinity")
            elif value["value"] == None:
                values.append("null")
            elif value["value"] == bool:
                values.append("[class Boolean]")
            elif value["value"] == dict:
                values.append("[class Object]")
            elif value["value"] == Exception:
                values.append("[class Error]")
            elif value["value"] == float or value == int:
                values.append("[class Number]")
            elif value["value"] == FunctionType:
                values.append("[class Function]")
            elif value["value"] == list:
                values.append("[class Array]")
            elif value["value"] == object:
                values.append("[class Attribute]")
            elif value["value"] == NoneType:
                values.append("Null")
            elif value["value"] == set:
                values.append("[class Set]")
            elif value["value"] == str:
                values.append("[class String]")
            elif value["value"] == tuple:
                values.append("[class Tuple]")
            elif isinstance(value["value"], FunctionType):
                values.append(f"[function {value['value'].__name__}]")
            elif isinstance(value["value"], type):
                values.append(repr(value["value"]))
            else:
                values.append(value["value"])
    print(*values)

def operatorRet(interpreter: Interpreter, module: Module, scope: Scope, section: list[list | str] | str, arguments: list[dict], *args, **kwargs) -> Any:
    scope.flgAdd("return")
    scope.value = arguments[0]["value"] if arguments else None
    return scope.value

def operatorSub(interpreter: Interpreter, module: Module, scope: Scope, section: list[list | str] | str, arguments: list[dict], *args, **kwargs) -> float | int | str:
    if len(arguments) < 2:
        raise Exceptions.ArgumentInvalid(f"Operator 'sub' takes at least 2 arguments")
    return arguments[0]["value"] - arguments[1]["value"]

# Exports
operators = [
    {
        "function": operatorAdd,
        "name": "add"
    },
    {
        "function": operatorBrk,
        "name": "brk"
    },
    {
        "function": operatorDiv,
        "name": "div"
    },
    {
        "function": lambda *args, **kwargs: None,
        "name": "end"
    },
    {
        "first": True,
        "function": operatorFunc,
        "name": "func",
        "raw": True,
        "section": True
    },
    {
        "function": operatorJmp,
        "name": "jmp"
    },
    {
        "function": operatorMod,
        "name": "mod"
    },
    {
        "function": operatorMul,
        "name": "mul"
    },
    {
        "function": operatorPrt,
        "name": "prt"
    },
    {
        "function": operatorRet,
        "name": "ret"
    },
    {
        "function": operatorSub,
        "name": "sub"
    }
]

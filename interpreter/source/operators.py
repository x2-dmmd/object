# Imports
from . import tools
from ..classes import Exceptions

# Operators
def oAdd(inpr, args, line, scope):
    if len(args) < 2:
        raise Exceptions.InvalidSyntaxException("Operator \"add\" requires two arguments", line = line, file = scope.file, highlight = "add")
    if args[0]["type"] == "null" and not tools.isValidName(args[0]["raw"]):
        raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[0]["raw"])
    if args[1]["type"] == "null" and not tools.isValidName(args[1]["raw"]):
        raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[1]["raw"])
    if args[0]["type"] == args[1]["type"] == "number":
        return str(tools.parseNumber(float(args[0]["value"]) + float(args[1]["value"])))
    elif args[0]["type"] == "string" or args[1]["type"] == "string":
        return f"\"{str(args[0]['value']) + str(args[1]['value'])}\""
    else:
        raise Exceptions.InvalidSyntaxException("Cannot add or append these two values", line = line, file = scope.file)

def oCmp(inpr, args, line, scope):
    if len(args) < 3:
        raise Exceptions.InvalidSyntaxException("Operator \"cmp\" requires three arguments", line = line, file = scope.file, highlight = "if")
    if args[0]["type"] == "null" and not tools.isValidName(args[0]["raw"]):
        raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[0]["raw"])
    if args[2]["type"] == "null" and not tools.isValidName(args[2]["raw"]):
        raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[2]["raw"])
    switcher = {
        "==": lambda a, b: a["value"] == b["value"],
        "!=": lambda a, b: a["value"] != b["value"],
        "<": lambda a, b: a["value"] < b["value"],
        "<=": lambda a, b: a["value"] <= b["value"],
        ">": lambda a, b: a["value"] > b["value"],
        ">=": lambda a, b: a["value"] >= b["value"],
        "typeof": lambda a, b: a["type"] == b["value"],
        "instanceof": lambda a, b: type(a["value"]) == b["value"] if a["type"] != "section" else False
    }
    comparator = switcher.get(args[1]["raw"], None)
    if comparator == None:
        raise Exceptions.InvalidSyntaxException("Invalid comparator", line = line, file = scope.file, highlight = args[1]["raw"])
    else:
        return "true" if comparator(args[0], args[2]) else "false"

def oDiv(inpr, args, line, scope):
    if len(args) < 2:
        raise Exceptions.InvalidSyntaxException("Operator \"add\" requires two arguments", line = line, file = scope.file, highlight = "add")
    if args[0]["type"] == "null" and not tools.isValidName(args[0]["raw"]):
        raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[0]["raw"])
    if args[1]["type"] == "null" and not tools.isValidName(args[1]["raw"]):
        raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[1]["raw"])
    if args[0]["type"] == args[1]["type"] == "number":
        return str(tools.parseNumber(float(args[0]["value"]) / float(args[1]["value"])))
    else:
        raise Exceptions.InvalidSyntaxException("Cannot divide these two values", line = line, file = scope.file)

def oEnd(inpr, args, line, scope):
    inpr.scope = inpr.stack.pop()
    if args:
        if args[0]["type"] == "null" and not tools.isValidName(args[0]["raw"]):
            raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[0]["raw"])
        return args[0]["value"]

def oIf(impr, args, line, scope):
    if not args:
        raise Exceptions.InvalidSyntaxException("Operator \"if\" requires one argument", line = line, file = scope.file, highlight = "if")
    return bool(args[0]["value"])


def oInp(inpr, args, line, scope):
    prompt = ""
    if args:
        if args[0]["type"] == "null" and not tools.isValidName(args[0]["raw"]):
            raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[0]["raw"])
        prompt = args[0]["value"]
    value = input(prompt)
    return f"\"{value}\""

def oJmp(inpr, args, line, scope):
    if not args:
        raise Exceptions.InvalidSyntaxException("Operator \"jmp\" requires one or more arguments", line = line, file = scope.file, highlight = "var")
    section = args[0]
    if section["type"] != "section":
        raise Exceptions.InvalidSyntaxException("Argument must be a section", line = line, file = scope.file, highlight = args[0]["raw"])
    inpr.stack.append(scope)
    inpr.scope = section["scope"]
    parameters = section["value"][0].split(" ")[1:]
    if len(args) - 1 < len(parameters):
        raise Exceptions.InvalidSyntaxException(f"Section expects {len(parameters)} parameters, got {len(args) - 1} instead", line = line, file = scope.file)
    for i in range(len(parameters)):
        if not tools.isValidName(parameters[i]):
            raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = section["value"][0], file = scope.file, highlight = parameters[i])
        if args[i + 1]["type"] == "null" and not tools.isValidName(args[i + 1]["raw"]):
            raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[i + 1]["raw"])
        scope.vSet(parameters[i], args[i + 1]["value"])
    inpr.loop(section["value"][1:-1], scope)
    end = section["value"][-1]
    if end.startswith("end"):
        return inpr.execute(end, inpr.scope)

def oMul(inpr, args, line, scope):
    if len(args) < 2:
        raise Exceptions.InvalidSyntaxException("Operator \"add\" requires two arguments", line = line, file = scope.file, highlight = "add")
    if args[0]["type"] == "null" and not tools.isValidName(args[0]["raw"]):
        raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[0]["raw"])
    if args[1]["type"] == "null" and not tools.isValidName(args[1]["raw"]):
        raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[1]["raw"])
    if args[0]["type"] == args[1]["type"] == "number":
        return str(tools.parseNumber(args[0]["value"]) * tools.parseNumber(args[1]["value"]))
    elif args[0]["type"] == "string" and args[1]["type"] == "number":
        return f"\"{args[0]['value'] * int(args[1]['value'])}\""
    else:
        raise Exceptions.InvalidSyntaxException("Cannot multiply these two values", line = line, file = scope.file)

def oPrt(inpr, args, line, scope):
    parsed, fancy = [], inpr.config.get("fancy")
    for arg in args:
        value = arg["value"]
        if not arg["raw"]:
            continue
        elif arg["type"] == "string":
            parsed.append(value)
        elif arg["type"] == "number":
            parsed.append(f"\033[33m{value}\033[0m" if fancy else value)
        elif arg["type"] == "boolean":
            value = "true" if value else "false"
            parsed.append(f"\033[33m{value}\033[0m" if fancy else value)
        elif arg["type"] == "section":
            name = value[0].split(" ")[0][1:]
            parsed.append(f"\033[96m[section {name}]\033[0m" if fancy else f"[class {name}]")
        elif arg["type"] == "class":
            parsed.append(f"\033[96m[class {value.__name__}]\033[0m" if fancy else f"[class {value.__name__}]")
        elif not tools.isValidName(args[0]["raw"]):
            raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = arg["raw"])
        elif arg["type"] == "null":
            parsed.append(f"\033[33mnull\033[0m" if fancy else "null")
    print(*parsed)

def oSub(inpr, args, line, scope):
    if len(args) < 2:
        raise Exceptions.InvalidSyntaxException("Operator \"add\" requires two arguments", line = line, file = scope.file, highlight = "add")
    if args[0]["type"] == "null" and not tools.isValidName(args[0]["raw"]):
        raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[0]["raw"])
    if args[1]["type"] == "null" and not tools.isValidName(args[1]["raw"]):
        raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[1]["raw"])
    if args[0]["type"] == args[1]["type"] == "number":
        return str(tools.parseNumber(float(args[0]["value"]) - float(args[1]["value"])))
    else:
        raise Exceptions.InvalidSyntaxException("Cannot subtract these two values", line = line, file = scope.file)

def oVar(inpr, args, line, scope):
    if not args:
        raise Exceptions.InvalidSyntaxException("Operator \"var\" requires one or more arguments", line = line, file = scope.file, highlight = "var")
    if not tools.isValidName(args[0]["raw"]):
        raise Exceptions.InvalidSyntaxException("Variable name contains illegal characters or is invalid", line = line, file = scope.file, highlight = args[0]["raw"])
    if len(args) == 1:
        return args[0]["value"]
    if scope.vHas(args[1]["raw"]):
        scope.vSet(args[0]["raw"], args[1]["value"], section = args[1]["section"], scope = scope)
    else:
        scope.vSet(args[0]["raw"], args[1]["raw"], scope = scope)
    return args[0]["raw"]

# Exports
operators = {
    "add": oAdd,
    "cmp": oCmp,
    "div": oDiv,
    "end": oEnd,
    "if": oIf,
    "inp": oInp,
    "jmp": oJmp,
    "mul": oMul,
    "prt": oPrt,
    "sub": oSub,
    "var": oVar
}
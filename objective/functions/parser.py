# Imports
from classes import Exceptions
from functions import tools
from string import ascii_letters, digits

# Variables
characterSet = ascii_letters + digits + "_"

# Functions
def parseArguments(tokens: list, module, scope) -> tuple:
    interpreter = scope.interpreter
    operator, *args = tokens
    if not interpreter.oHas(operator):
        raise Exceptions.OperatorNotFound(f"Cannot find operator '{operator}'")
    arguments = []
    for i in range(len(args)):
        data = {
            "raw": args[i]
        }
        if tools.isNumber(args[i]):
            data["value"] = parseNumber(args[i])
        elif len(args[i]) > 1 and ((args[i].startswith("\"") and args[i].endswith("\"")) or (args[i].startswith("'") and args[i].endswith("'"))):
            data["value"] = args[i][1:-1]
        elif len(args[i]) > 1 and args[i].startswith("(") and args[i].endswith(")"):
            data["value"] = scope.interpreter.executeLine(args[i][1:-1], module, scope)
        else:
            data["value"] = scope.vGet(args[i])
        arguments.append(data)
    return operator, arguments

def parseFields(lines: list) -> list:
    fieldStack = []
    fields = []
    field = fields
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith(("class ", "if ", "repeat ", "sect ", "while ")):
            subfield = []
            fieldStack.append(field)
            field.append(subfield)
            field = subfield
        if line.startswith("end ") or line == "end":
            if not fieldStack:
                raise Exceptions.FieldUnderflow("Cannot end the module scope (Perhaps you placed an extra 'end' somewhere?)")
            field = fieldStack.pop()
        else:
            field.append(line)
    if fieldStack:
        raise Exceptions.FieldOverflow("Unterminated scope (Perhaps you forgot to place an 'end' somewhere?)")
    return fields

def parseFile(path: str) -> list:
    return parseFields(parseLines(path))

def parseLine(line, module, scope) -> tuple:
    return parseArguments(parseTokens(line), module, scope)

def parseLines(path: str) -> list:
    with open(path, "r") as file:
        content = file.read()
    lines = []
    line = ""
    comment = False
    string = None
    previous = ""
    for character in content:
        if character == "\n" and not string:
            lines.append(line)
            line = ""
            comment = False
            string = None
            previous = ""
        elif character == ":" and previous == ":" and not string:
            if not comment:
                line = line[:-2]
            comment = not comment
        elif comment:
            pass
        elif character == "\n" and string and previous == "\\":
            line = line[:-1]
        elif character in ["\"", "'"] and previous != "\\":
            if string and character == string:
                string = None
            elif not string:
                string = character
            line += character
        else:
            line += character
        previous = character
    if line:
        lines.append(line)
    return lines

def parseNumber(string: str) -> float | int:
    if not tools.isNumber(string):
        raise Exceptions.BadToken(f"Invalid number format '{string}'")
    number = float(string)
    return int(number) if number.is_integer() else number

def parseTokens(line: str) -> list:
    wrapper = None
    previous = ""
    tokens = []
    token = ""
    for character in line:
        if character == " " and not wrapper:
            if token:
                tokens.append(token)
            wrapper = None
            previous = ""
            token = ""
        elif character == "\"" and wrapper in ["double", None] and previous != "\\":
            wrapper = None if wrapper else "double"
            token += character
        elif character == "'" and wrapper in ["single", None] and previous != "\\":
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
        previous = character
    if token:
        tokens.append(token)
    for token in tokens:
        if not token.startswith(("\"", "'", "(")) and not tools.isNumber(token) and (not token[0].isalpha() or any([character not in characterSet for character in token])):
            raise Exceptions.BadToken(f"Unexpected token: {token}")
    return tokens
            
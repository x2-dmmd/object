# Imports
import re

# Functions
def isNumber(value):
    return bool(re.match(r"^[+-]?((\d+\.?)|(\d*\.\d+))$", str(value), flags = 0))

def isValidName(value):
    return bool(re.match(r"[a-zA-Z][a-zA-Z0-9]*", str(value), flags = 0))

def parseNumber(value):
    if not isNumber(value):
        raise Exception("Value is not a number")
    number = float(value)
    if number.is_integer():
        number = int(number)
    return number

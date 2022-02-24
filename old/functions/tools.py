# Imports
import re
import string
from classes import Exceptions
from classes.Scope import Scope
from typing import Any

# Variables
characters = string.ascii_letters + string.digits + "_"

# Functions
def isNumber(string: str) -> bool:
    return bool(re.match(r"^[+-]?((\d+\.?\d*)|(\d*\.\d+))$", string))
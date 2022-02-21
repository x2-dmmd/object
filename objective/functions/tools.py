# Imports
import re
from classes import Exceptions
from classes.Scope import Scope
from typing import Any

# Functions
def isNumber(string: str) -> bool:
    return bool(re.match(r"^[+-]?((\d+\.?\d*)|(\d*\.\d+))$", string))
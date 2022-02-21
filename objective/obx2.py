# Imports
import json
import os
import sys
from classes import Exceptions
from classes.Interpreter import Interpreter
from functions.operators import operators
from types import NoneType

# Variables
argv = sys.argv[1:]
config = {}
constants = {
    "array": list,
    "false": False,
    "null": None,
    "Null": NoneType,
    "object": dict,
    "true": True
}
installation = os.path.dirname(__file__)
with open(os.path.join(installation, "build.json")) as file:
    build = json.loads(file.read())
if os.path.isfile(".xtconfig"):
    with open(".xtconfig", "r") as file:
        config = json.loads(file.read())


# Executes
try:
    # Command-Line Interface
    if not argv:
        print("Objective x2 Environment: Coming Soon™")
        sys.exit(1)
    if argv[0].startswith("-"):
        if argv[0] in ["-h", "--help"]:
            with open(os.path.join(installation, "texts/help.txt")) as file:
                content = file.read()
            sys.exit(content if len(argv) > 1 and argv[1] in ["-l", "--long"] else content.split("\n\n")[0])
        if argv[0] in ["-i", "--installation"]:
            sys.exit(installation)
        if argv[0] in ["-v", "--ver", "--version"]:
            sys.exit(build["version"])
        raise Exceptions.BadOption(f"Cannot parse option '{' '.join(argv)}'")

    # Executes File
    for flag in argv[1:]:
        if flag in ["-f", "--fancy"]:
            config["fancy"] = True
        elif flag in ["-nf", "--nofancy"]:
            config["fancy"] = False
        elif flag in ["-nq", "--noquiet"]:
            config["quiet"] = False
        elif flag in ["-q", "--q"]:
            config["quiet"] = True
        else:
            raise Exceptions.BadFlag(f"Cannot parse flag '{flag}'")
    interpreter = Interpreter(build, config)
    for oKey, oValue in operators.items():
        interpreter.oSet(oKey, oValue)
    for vKey, vValue in constants.items():
        interpreter.vSet(vKey, vValue, True, True)
    interpreter.mImport(config.get("main", "main.obx2") if argv[0] == "." else argv[0])

# Exceptions
except KeyboardInterrupt:
    sys.exit(0)
except Exceptions.InterpreterException as InterpreterException:
    sys.exit(0 if config.get("quiet") == True else repr(InterpreterException))
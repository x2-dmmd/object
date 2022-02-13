# Imports
from .classes import Exceptions
from .classes.Interpreter import Interpreter
from .source.operators import operators
import json
import os
import sys

# DEBUG IMPORTS
# from rich import print

# Variables
argv = sys.argv[1:]
localPath = os.path.dirname(__file__)
with open(os.path.join(localPath, "build.json")) as file:
    build = json.loads(file.read())

# Argument Parser
if not argv:
    print("Environment coming soon")
    sys.exit(0)

if "-h" == argv[0] or "--help" == argv[0]:
    print("Usage:")
    print("  x2 [ script.xt ] [ ...arguments ]")
    print("  x2 [ options ]")
    print()
    print("Options:")
    print("  -h, --help\n\tDisplays help menu")
    print("  -v, --version\n\tPrints x2 version")
    sys.exit(0)

elif "-v" == argv[0] or "--version" == argv[0]:
    print(build["version"])
    sys.exit(0)

# Interpreter
try:
    config = {}
    if os.path.isfile(".xtconfig"):
        with open(".xtconfig", "r") as file:
            config = json.loads(file.read())
    if argv[0] == ".":
        argv[0] = config.get("main", "main.oxt")
    if not os.path.isfile(argv[0]):
        raise Exceptions.UnknownFileException("Cannot find file in the current working directory", highlight = argv[0])
    interpreter = Interpreter(build, config)
    for key, value in operators.items():
        interpreter.oSet(key, value)
    interpreter.run(argv[0])

except KeyboardInterrupt:
    print("x2 process exited: 0")
    sys.exit(0)

except Exceptions.InterpreterException as RunTimeException:
    if not config.get("quiet"):
        print(repr(RunTimeException))
    sys.exit(1)
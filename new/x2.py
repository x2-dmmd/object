# Imports
import json
import os
import sys
from .classes import Global, Errors

# Global Variables
local = os.path.dirname(__file__)
with open(os.path.join(local, "build.json"), "r") as file:
    build = json.loads(file.read())
config = {}
if os.path.isfile(".xtconfig"):
    with open(".xtconfig", "r") as file:
        config = json.loads(file.read())

# CLI
argv = sys.argv[1:]

if argv[0] in ["-h", "--help"]:
    print("=== x2 Help ===")
    print("Usage:")
    print("  x2 [options]")
    print("  x2 [file]")
    print()
    print("Options")
    print("  -h, --help\n\tDisplays this menu")
    print("  -p, --path\n\tPrints x2 installation path")
    print("  -v, --ver, --version\n\tPrints x2 version")
    sys.exit(0)

if argv[0] in ["-p", "--path"]:
    print(local)
    sys.exit(0)

if argv[0] in ["-v", "--ver", "--version"]:
    print(build["version"])
    sys.exit(0)

# Runs File
try:
    file = config.get("main", "main.oxt") if argv[0] == "." else argv[0]
    if not os.path.isfile(file):
        raise Errors.FileNotFound(f"Cannot find file '{file}'")
    Global.Global().load(file)
except KeyboardInterrupt:
    print("x2 exited: 0")
    sys.exit(0)
except Errors.x2Error as error:
    print(repr(error))
    sys.exit(1)
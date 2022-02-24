# Imports
import os
import sys
from classes import Exceptions, Components
from src.commands import commands
from src.constants import constants
from src.operators import operators

# Executes
argv = sys.argv[1:]
interpreter = Components.Interpreter()
try:
    for data in commands:
        interpreter.register.registerCommand(**data)
    for key, value in constants.items():
        interpreter.globalScope.varSet(key, value, True, True)
    for data in operators:
        interpreter.register.registerOperator(**data)
    if not argv:
        print("Objective x2 Environment: Coming Soon")
        sys.exit(0)
    elif argv[0].startswith("-"):
        interpreter.executeCommand(argv, commandType = "option")
        sys.exit(0)
    flags = []
    flag = []
    for arg in argv[1:]:
        if arg.startswith("-") and flag:
            flags.append(flag)
            flag = []
        flag.append(arg)
    if flag:
        flags.append(flag)
    for flag in flags:
        interpreter.executeCommand(flag, commandType = "flag")
    interpreter.register.registerModule(interpreter.config.get("main", "main.obx2") if argv[0] == "." else argv[0])
except KeyboardInterrupt:
    sys.exit(0)
except Exceptions.InterpreterException as InterpreterException:
    if interpreter.config.get("debug"):
        raise InterpreterException
    if not interpreter.config.get("quiet") and not interpreter.config.get("ignoreInterpreterExceptions"):
        print(repr(InterpreterException))
    sys.exit(1)
except Exception as PythonException:
    if interpreter.config.get("debug"):
        raise PythonException
    if not interpreter.config.get("quiet") and not interpreter.config.get("ignorePythonExceptions"):
        print(f"{PythonException.__class__.__name__}: {PythonException}")
    sys.exit(1)

# Imports
import os
from classes import Exceptions
from classes.Components import Interpreter

# Functions
def commandDebug(interpreter: Interpreter, command: list[str], commandType: str | None = None, *args, **kwargs) -> bool:
    if commandType == "flag":
        interpreter.config["debug"] = command[0] == command[0].lower()
        return interpreter.config["debug"]
    else:
        raise Exceptions.CommandInvalid(f"Command 'debug' can only be used as a flag", command = " ".join(command))

def commandFancy(interpreter: Interpreter, command: list[str], commandType: str | None = None, *args, **kwargs) -> bool:
    if commandType == "flag":
        interpreter.config["fancy"] = command[0] == command[0].lower()
        return interpreter.config["fancy"]
    else:
        raise Exceptions.CommandInvalid(f"Command 'fancy' can only be used as a flag", command = " ".join(command))

def commandHelp(interpreter: Interpreter, command: list[str], commandType: str | None = None, *args, **kwargs) -> None:
    if commandType == "option":
        with open(os.path.join(interpreter.path, "texts/help.txt"), "r") as file:
            content = file.read()
        print(content if len(command) > 1 and command[1] in ["-l", "--long"] else content.split("\n\n\n")[0])
    else:
        raise Exceptions.CommandInvalid(f"Command 'help' can only be used as an option", command = " ".join(command))

def commandIgnoreInterpreterExceptions(interpreter: Interpreter, command: list[str], commandType: str | None = None, *args, **kwargs) -> None:
    if commandType == "flag":
        interpreter.config["ignoreInterpreterExceptions"] = command[0] == command[0].lower()
        return interpreter.config["ignoreInterpreterExceptions"]
    else:
        raise Exceptions.CommandInvalid(f"Command 'ignoreInterpreterExceptions' can only be used as a flag", command = " ".join(command))

def commandIgnorePythonExceptions(interpreter: Interpreter, command: list[str], commandType: str | None = None, *args, **kwargs) -> None:
    if commandType == "flag":
        interpreter.config["ignorePythonExceptions"] = command[0] == command[0].lower()
        return interpreter.config["ignorePythonExceptions"]
    else:
        raise Exceptions.CommandInvalid(f"Command 'ignorePythonExceptions' can only be used as a flag", command = " ".join(command))

def commandPath(interpreter: Interpreter, command: list[str], commandType: str | None = None, *args, **kwargs) -> None:
    if commandType == "option":
        print(interpreter.path)
    else:
        raise Exceptions.CommandInvalid(f"Command 'path' can only be used as an option", command = " ".join(command))

def commandQuiet(interpreter: Interpreter, command: list[str], commandType: str | None = None, *args, **kwargs) -> bool:
    if commandType == "flag":
        interpreter.config["quiet"] = command[0] == command[0].lower()
        return interpreter.config["quiet"]
    else:
        raise Exceptions.CommandInvalid(f"Command 'quiet' can only be used as a flag", command = " ".join(command))

def commandVersion(interpreter: Interpreter, command: list[str], commandType: str | None = None, *args, **kwargs) -> None:
    if commandType == "option":
        print(interpreter.build["version"])
    else:
        raise Exceptions.CommandInvalid(f"Command 'version' can only be used as an option", command = " ".join(command))

# Exports
commands = [
    {
        "function": commandDebug,
        "names": ["-d", "--debug", "-D", "--DEBUG"]
    },
    {
        "function": commandFancy,
        "names": ["-f", "--fancy", "-F", "--FANCY"]
    },
    {
        "function": commandHelp,
        "names": ["-h", "--help"]
    },
    {
        "function": commandIgnoreInterpreterExceptions,
        "names": ["-iip", "--ignoreinterpreter", "--ignoreinterpreterexceptions", "-IIP", "--IGNOREINTERPRETER", "--IGNOREINTERPRETEREXCEPTIONS"]
    },
    {
        "function": commandIgnorePythonExceptions,
        "names": ["-ipy", "--ignorepython", "--ignorepythonexceptions", "-IPY", "--IGNOREPYTHON", "--IGNOREPYTHONEXCEPTIONS"]
    },
    {
        "function": commandPath,
        "names": ["-p", "--path"]
    },
    {
        "function": commandQuiet,
        "names": ["-q", "--quiet", "-Q", "--QUIET"]
    },
    {
        "function": commandVersion,
        "names": ["-v", "--ver", "--version"]
    }
]

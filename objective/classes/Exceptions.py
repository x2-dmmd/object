# Classes
class InterpreterException(Exception):
    def __init__(self, message: str, fields: dict = {}, **kwargs) -> None:
        super().__init__(message)
        self.message = message
        self.fields = {**fields, **kwargs}

    def __repr__(self) -> str:
        exception = f"{self.__class__.__name__}: {self.message}"
        for field in self.fields.items():
            exception += f"\n  At {field[0]}: {field[1]}"
        return exception

class ArgumentInvalid(InterpreterException):
    pass

class CommandInvalid(InterpreterException):
    pass

class CommandNotFound(InterpreterException):
    pass

class ConstantDelete(InterpreterException):
    pass

class ConstantSet(InterpreterException):
    pass

class FunctionOperatorBreak(InterpreterException):
    pass

class ModuleOperatorBreak(InterpreterException):
    pass

class ModuleOperatorReturn(InterpreterException):
    pass

class ModuleNotFound(InterpreterException):
    pass

class OperatorNotFound(InterpreterException):
    pass

class SectionOverflow(InterpreterException):
    pass

class SectionUnderflow(InterpreterException):
    pass

class TokenInvalid(InterpreterException):
    pass

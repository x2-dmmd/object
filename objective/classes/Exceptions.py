# Class
class InterpreterException(Exception):
    def __init__(self, message: str, **kwargs) -> None:
        super().__init__(message)
        self.data = kwargs
        self.message = message
        self.type = self.__class__.__name__
    
    def __repr__(self) -> str:
        string = f"{self.type}: {self.message}"
        for key, value in self.data.items():
            string += f"\n\t{key}: {value}"
        return string

class ArgumentMissing(InterpreterException):
    pass

class ArgumentType(InterpreterException):
    pass

class BadFlag(InterpreterException):
    pass

class BadOption(InterpreterException):
    pass

class BadToken(InterpreterException):
    pass

class BranchOverflow(InterpreterException):
    pass

class ConstantAssignment(InterpreterException):
    pass

class FieldOverflow(InterpreterException):
    pass

class FieldUnderflow(InterpreterException):
    pass

class ModuleConflict(InterpreterException):
    pass

class ModuleNotFound(InterpreterException):
    pass

class ModuleReturn(InterpreterException):
    pass

class OperatorNotFound(InterpreterException):
    pass

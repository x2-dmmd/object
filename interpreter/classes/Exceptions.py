# Exceptions
class InterpreterException(Exception):
    def __init__(self, message = None, line = None, file = None, highlight = None):
        Exception.__init__(self, message)
        self.message = message
        self.line = line
        self.file = file
        self.highlight = highlight

    def __repr__(self):
        lineFeed = "\n  "
        message = f"{self.message}{f': {self.highlight}' if self.highlight else ''}"
        if self.line:
            message += f"{lineFeed}At line: {self.line}"
        if self.file:
            message += f"{lineFeed}At file: {self.file}"
        return message

class ConstantVariableException(InterpreterException):
    pass

class InvalidSectionException(InterpreterException):
    pass

class InvalidSyntaxException(InterpreterException):
    pass

class UnknownSyntaxException(InterpreterException):
    pass

class UnknownFileException(InterpreterException):
    pass

class UnknownOperatorException(InterpreterException):
    pass

class UndefinedVariableException(InterpreterException):
    pass

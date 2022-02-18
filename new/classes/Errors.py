# Classes
class x2Error(Exception):
    def __init__(self, message: str, **kwargs) -> None:
        self.message = message
        self.info = kwargs

    def __repr__(self) -> str:
        message = self.message
        for key, value in self.info.items():
            message += f"\n  At {key}: {value}"
        return message

class ConstantVariable(x2Error):
    pass

class FileNotFound(x2Error):
    pass

class InvalidStack(x2Error):
    pass

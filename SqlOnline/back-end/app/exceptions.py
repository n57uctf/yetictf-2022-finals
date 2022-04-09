class NotAllowedDatatypeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class NotAllowedCharacterException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class DatabaseAlreadyExistException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AppException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
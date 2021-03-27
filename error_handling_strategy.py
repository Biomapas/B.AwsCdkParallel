from enum import Enum, auto


class ErrorHandlingStrategy(Enum):
    RETRY = auto()
    RAISE = auto()
    DO_NOTHING = auto

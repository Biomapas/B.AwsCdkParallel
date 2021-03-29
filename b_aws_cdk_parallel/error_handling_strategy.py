from enum import Enum, auto


class ErrorHandlingStrategy(Enum):
    RETRY = auto()
    RETRY_IF_POSSIBLE = auto()
    RAISE = auto()
    DO_NOTHING = auto()

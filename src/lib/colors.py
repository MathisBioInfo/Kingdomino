from enum import Enum


class Colors(Enum):
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"

    def __call__(self, string):
        return f"{self.value}{string}\033[0m"

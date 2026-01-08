DEBUG = False

_RESET = "\033[0m"
_COLORS = {
    "warn": "\033[33m",
    "err": "\033[31m",
}


def set_debug():
    global DEBUG
    DEBUG = True


def _log(color, *args, **kwargs):
    if DEBUG:
        print(f"{color}", end="")
        print(*args, **kwargs)
        print(f"{_RESET}", end="")


def log(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def warn(*args, **kwargs):
    _log(_COLORS["warn"], *args, **kwargs)


def err(*args, **kwargs):
    _log(_COLORS["err"], *args, **kwargs)

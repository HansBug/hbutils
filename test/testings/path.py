import os.path


def normpath(path: str) -> str:
    return os.path.normcase(os.path.normpath(os.path.abspath(path)))

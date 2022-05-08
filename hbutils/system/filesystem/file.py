"""
Overview:
    Functions for file processing.
"""
import os
import pathlib

__all__ = [
    'touch',
]


def touch(file: str, exist_ok: bool = True, makedirs: bool = True):
    """
    Overview:
        Touch the file at given path.
        Just like the ``touch`` command in unix system.

    :param file: Path of the file.
    :param exist_ok: Exist is okay or not.
    :param makedirs: Create directories when necessary.
    """
    if makedirs:
        path, _ = os.path.split(file)
        os.makedirs(path, exist_ok=exist_ok)
    pathlib.Path(file).touch(exist_ok=exist_ok)

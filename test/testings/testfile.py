import os.path

_LOCAL_DIR, _ = os.path.split(os.path.abspath(__file__))


def get_testfile_path(path: str) -> str:
    return os.path.normpath(os.path.join(_LOCAL_DIR, '..', 'testfile', path))


def get_testfile_igm_path(path: str) -> str:
    return get_testfile_path(os.path.join('igm', path))

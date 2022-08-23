from pip._internal.models.link import Link
from pip._internal.utils.misc import hide_url
from pip._internal.vcs import vcs
from pip._internal.vcs.versioncontrol import VersionControl


def _get_vcs_backend(url: str) -> VersionControl:
    return vcs.get_backend_for_scheme(Link(url).scheme)


def is_vcs_url(url: str) -> bool:
    """
    Overview:
        Check if the given ``url`` is a vcs-based url.

    :param url: Url to be checked.
    :return: Given ``url`` is vcs-based or not.
    """
    vcs_backend = _get_vcs_backend(url)
    return bool(Link(url).is_vcs and vcs_backend)


class InvalidVCSURL(Exception):
    """
    Overview:
        Invalid url for VCS (Version Control System).
    """
    pass


def retrieve_from_vcs(url: str, dstpath: str, verbosity: int = 1):
    """
    Retrieve source path from version control system.

    :param url: Url of vcs, which have the same format in ``pip install``.
    :param dstpath: Local Destination path.
    :param verbosity: Verbosity level of the retrieve, default is ``1``.
    :return: Destination path.
    """
    if not is_vcs_url(url):
        raise InvalidVCSURL(url)

    vcs_backend = _get_vcs_backend(url)
    vcs_backend.obtain(dstpath, hide_url(url), verbosity)
    return dstpath

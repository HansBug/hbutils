from .model import Dependency


def parse_dependency(dep: str) -> Dependency:
    """
    Overview:
        Parse dependency line.

        See :meth:`hbutils.dependency.model.Dependency.loads`.


    :param dep: Dependency line.
    :return: Parsed dependency object.
    """
    return Dependency.loads(dep)

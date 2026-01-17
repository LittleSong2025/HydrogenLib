import typing


def _bind_py_type(pytype, ctype):
    if typing.TYPE_CHECKING:
        return pytype
    else:
        return ctype

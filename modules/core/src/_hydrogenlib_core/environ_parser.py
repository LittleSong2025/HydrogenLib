import contextlib
import os
from typing import Callable, Any, MutableMapping

list_sep = ';' if os.name == 'nt' else ':'

type EnvironType = MutableMapping[str, str]
type TypeCallable[P=Any, R=Any] = Callable[[P], R]


def pathlist(path_string: str):
    return path_string.split(list_sep)


class Environ:
    def __init__(self, environ: EnvironType):
        self.environ = environ

    def get(self, key: str, default: Any = None):
        return self.environ.get(key, default)

    def parsed(self, key: str, type: TypeCallable[str, Any]):
        return type(self[key])

    def to_dict(self):
        return dict(self.environ)

    def update(self, m=None, **kwargs):
        self.environ.update(m, **kwargs)

    def copy(self):
        return dict(self.environ)

    def __getitem__(self, item):
        return self.environ[item]

    def __setitem__(self, key, value):
        self.environ[key] = value

    def __delitem__(self, key):
        del self.environ[key]

    def __contains__(self, item):
        return item in self.environ

    def __iter__(self):
        return self.environ.__iter__()


class EnvironVar[T, DT]:
    def __init__(self, environ: Environ, name: str, default: DT = None, type: TypeCallable[str, T] = None):
        self.environ = environ
        self.name = name
        self.default = default
        self.type = type

    def check_name(self):
        if self.name is None:
            raise RuntimeError('No environ name')

    def get(self) -> T | DT:
        self.check_name()
        if self.name not in self.environ:
            return self.default

        else:
            value = self.environ[self.name]
            return self.type(value) if self.type else value

    def set(self, value: str):
        self.check_name()
        self.environ[self.name] = value

    def delete(self):
        self.check_name()
        if self.name in self.environ:
            del self.environ[self.name]


class environ_property[T]:
    def __init__(self, environ: Environ, name: str = None, default: Any = None, type: TypeCallable[str, T] = None,
                 set_convertor: Callable[[Any], str] = None):
        self.var = EnvironVar(environ, name, default, type)
        self.set_convertor = set_convertor or (lambda value: value)

    def __set_name__(self, owner, name):
        self.var.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.var.get()

    def __set__(self, instance, value):
        return self.var.set(
            self.set_convertor(value)
        )

    def __delete__(self, instance):
        self.var.delete()


environ = Environ(dict(os.environ))


def update_environ(environ):
    os.environ.update(environ)


def reset_environ(environ):
    os.environ.clear()
    os.environ.update(environ)


@contextlib.contextmanager
def with_environ(environ: EnvironType | Environ):
    """
    环境变量上下文管理器

    :param environ: 过程中保持的环境变量
    :return:
    """
    if not isinstance(environ, Environ):
        environ = Environ(environ)

    environ_backup = os.environ.copy()
    reset_environ(environ)
    yield environ
    reset_environ(environ_backup)

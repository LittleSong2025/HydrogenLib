import ctypes
import inspect
from functools import wraps

from ._func import c_function
from ._types import _Ctype


class _DLLMeta(type):
    def __getattr__(self, item) -> 'DLL':
        return self(item)


class DLL(metaclass=_DLLMeta):
    def __init__(self, name: str):
        self._name = name
        self._dll = ctypes.CDLL(self._name)

    def value(self, name: str, type):
        type = _Ctype.as_ctype(type)
        return type.in_dll(self._dll, name)

    def __call__(self, maybe_func=None, *, name: str = None):
        def decorator(func):
            nonlocal name
            name = name or func.__name__

            prototype = c_function(name=name)(func)
            func_ptr = prototype(getattr(
                self._dll, name
            ))
            signature = inspect.signature(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                bound_args = signature.bind(*args, **kwargs)
                bound_args.apply_defaults()
                return func_ptr(
                    *bound_args.args, **bound_args.kwargs
                )

            return wrapper

        return decorator if not maybe_func else decorator(maybe_func)

from typing import Callable, Any, overload

type Getter[T] = Callable[[...], T]
type Setter[T] = Callable[[Any, T], None]
type Deleter = Callable[[...], None]


class lazy_property[T]:  # Copy from functools.cached_property
    fget: Getter[T]
    fset: Setter[T]
    fdel: Deleter

    def getter(self, fget: Getter[T]) -> T:
        ...

    def setter(self, fset: Setter[T]) -> None: ...

    def deleter(self, fdel: Deleter) -> None: ...

    @overload
    def __init__(self, fget: Getter[T]) -> None: ...

    @overload
    def __init__(self, fget: Getter[T], fset: Setter[T], fdel: Deleter) -> None: ...

    @overload
    def __get__(self, instance: None, owner: type[Any] | None = None) -> Self: ...

    @overload
    def __get__(self, instance: object, owner: type[Any] | None = None) -> T: ...

    def __set_name__(self, owner: type[Any], name: str) -> None: ...

    def __set__(self, instance: object,
                value: T) -> None: ...  # type: ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]

import datetime

from . import core
from _hydrogenlib_core.typefunc import builtin_types

global_type_registry = core.type_registry.TypeRegistry()
register_self_validating_type = global_type_registry.register_self_validating_type

register_self_validating_type(
    list(filter(lambda x: x is not None, builtin_types))
)

@global_type_registry.add_validator(to=datetime.datetime)
def datetime_validator(value, target_type, subtypes):
    if isinstance(value, str):
        return datetime.datetime.fromisoformat(value)
    elif isinstance(value, datetime.datetime):
        return value
    elif isinstance(value, (int, float)):
        return datetime.datetime.fromtimestamp(value)

    raise ValueError(f"Invalid datetime type: {type(value)}")

@global_type_registry.add_validator(to=datetime.date)
def date_validator(value, target_type, subtypes):
    if isinstance(value, str):
        return datetime.date.fromisoformat(value)
    elif isinstance(value, datetime.date):
        return value
    elif isinstance(value, (int, float)):
        return datetime.date.fromtimestamp(value)

    raise ValueError(f"Invalid datetype: {type(value)}")


global_type_registry.add_validator(to=object)(
    lambda x: x  # 这玩意有啥好验证的
)

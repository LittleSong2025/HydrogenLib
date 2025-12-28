from __future__ import annotations

import builtins
import dataclasses
from typing import Any, Callable

from _hydrogenlib_core.typefunc import AutoSlots
from .type_registry import TypeRegistry, validate


@dataclasses.dataclass
class FieldInfo:
    name: str = None
    type: builtins.type = None
    default: Any = None
    default_factory: Callable = None
    validator: Callable[[Any], type] = None
    extra_validators: list[Callable[[Any], type]] = dataclasses.field(
        default_factory=list
    )
    alias: str = None


class Field(AutoSlots):
    field_info: FieldInfo
    value: Any

    def __init__(self, field_info: FieldInfo):
        super().__init__()
        self.field_info = field_info
        self.value = self.default

    @property
    def default(self):
        return (
            self.field_info.default_factory()
            if self.field_info.default_factory is not None
            else self.field_info.default
        )

    @property
    def key(self):
        return self.field_info.alias or self.field_info.name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.value

    def __set__(self, instance, value):
        info = self.field_info

        if info.validator is not None:  # 首先检查是否有专用的验证器
            value = info.validator(value)  # 有，执行验证
        elif (tr := getattr(instance, "__config_type_registry__")) is not None:  # 否则查看容器的类型注册表
            tr: TypeRegistry
            try:
                value = validate(  # 有效，尝试从注册表执行验证函数
                    tr, value, info.type
                )
            except KeyError:
                pass  # 注册表内没有符合这个类型的验证函数
        # 否则不执行验证
        for i in info.extra_validators:  # 执行所有拓展验证器
            if i(value) is False:
                raise RuntimeError("Validating failed")
            # 拓展验证器无法修改值，只能用于验证数据的正确性

        self.value = value

    def __del__(self):
        self.value = self.default

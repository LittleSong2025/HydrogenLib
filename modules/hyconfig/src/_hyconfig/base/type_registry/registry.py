from typing import Callable, Any

from _hycore.utils import InstanceMapping

type Validator = Callable[[Any], Any]


class TypeRegistry:
    def __init__(self, mro=None):
        self._mro = mro or InstanceMapping()  # type: InstanceMapping[type, InstanceMapping[type, Validator]]

    def validate(self, data, target: type):
        sources = type(data).__mro__
        for source in sources:
            if self.exists(source, target):
                return self.get(source, target)(data)

    def register(self, source: type, target: type, method: Validator):
        if source not in self._mro:
            self._mro[source] = InstanceMapping()

        self._mro[source][target] = method

    def get(self, source: type, target: type):
        if not self.exists(source, target):
            return None
        return self._mro[source][target]

    def unregister(self, source: type, target: type):
        if not self.exists(source, target):
            return
        del self._mro[source][target]

    def exists(self, source: type, target: type):
        return source in self._mro and target in self._mro[source]

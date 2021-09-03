from array import array
from typing import Any
import reprlib
import math
import numbers
import functools
import operator
import itertools


class Vector:
    typecode = 'd'

    def __init__(self, components) -> None:
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self) -> str:
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return f'Vector({components})'

    def __str__(self) -> str:
        return str(tuple(self))

    def __bytes__(self) -> tuple:
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    def __eq__(self, other: object) -> bool:
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self) -> int:
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self) -> float:
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self) -> bool:
        return bool(abs(self))

    def __len__(self) -> int:
        return len(self._components)

    def __getitem__(self, index) -> float:
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        msg = f'{cls.__name__} indices must be integers'
        raise TypeError(msg)

    shortcut_names = 'xyzt'

    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = f'{cls.__name__!r} object has no attribute {name!r}'
        raise AttributeError(msg)

    def __setattr__(self, name: str, value: Any) -> None:
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = f'readonly attribute {name!r}'
            elif name.islower():
                error = f"can't set attributes 'a' to 'z' in {cls.__name__!r}"
            else:
                error = ''
            if error:
                raise AttributeError(error)
        super().__setattr__(name, value)

    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):  # 超球面坐标
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.join(components))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

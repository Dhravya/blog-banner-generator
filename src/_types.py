from collections import namedtuple

class Coordinates(namedtuple('Coordinates', ['x', 'y', 'size'])):
    __slots__ = ()

    def __new__(cls, x, y, size:tuple=(0, 0)):
        return super().__new__(cls, x, y, size)

rgb = namedtuple("rgb", ['r', 'g', 'b'])
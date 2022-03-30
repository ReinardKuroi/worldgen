import numpy
import logging

from scipy.special import expit
from skimage.measure import marching_cubes


def distance(a: numpy.array, b: numpy.array):
    return numpy.linalg.norm(b - a)


class MeshData3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.data = numpy.zeros((x, y, z))
        self.grid = numpy.meshgrid(*(numpy.arange(s) for s in self.data.shape), indexing='ij')
        self._diagonal = self.data.diagonal()
        self.__marching_func = marching_cubes

    @property
    def max_value(self):
        return numpy.max(self.data)

    def _apply_function(self, func):
        self.data = func(self.data)

    def create_scalar_field_from_function(self, func):
        if not isinstance(func, numpy.vectorize):
            func = numpy.vectorize(func)
        return func(*self.grid)

    def normalize(self):
        self._apply_function(expit)

    def set_point(self, x, y, z, value):
        self.data[x, y, z] = value
        logging.debug(f'Set [{x}, {y}, {z}] = {value}')

    def get_point(self, x, y, z):
        return self.data[x, y, z]

    def march(self, **kwargs):
        return self.__marching_func(self.data, **kwargs)


class MeshData2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.data = numpy.array((x, y))

    def iterate(self):
        for x in range(self.x):
            for y in range(self.y):
                yield x, y

    def set_point(self, x, y, value):
        self.data[x, y] = value

    def get_point(self, x, y):
        return self.data[x, y]

    def apply_function(self, func):
        for x, y in self.iterate():
            value = func(x, y)
            self.set_point(x, y, value)

    def to_3d(self, z_max) -> MeshData3D:
        volumetric_data = MeshData3D(self.x, self.y, z_max)
        for x, y in self.iterate():
            value = self.get_point(x, y)

        return volumetric_data


def expand_float_to_linear(value: float) -> numpy.ndarray:
    length: int = numpy.ceil(value).astype(int)
    linear: numpy.ndarray = numpy.ones(length,)
    linear[-1] = value - length + 1
    return linear


def extend_linear_to_length(linear: numpy.ndarray, length: int) -> numpy.ndarray:
    linear.resize((length,))


def test_iteration(array: numpy.ndarray):
    x_dim, y_dim, z_dim = array.shape
    for x in range(x_dim):
        for y in range(y_dim):
            for z in range(z_dim):
                a = array[x, y, z]


def test_nditer(array: numpy.ndarray):
    with numpy.nditer(array, flags=['multi_index']) as field:
        for point in field:
            point[...] = point


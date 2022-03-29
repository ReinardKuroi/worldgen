import numpy
import logging

from skimage.measure import marching_cubes


def distance(a: numpy.array, b: numpy.array):
    return numpy.linalg.norm(b - a)


class MeshData3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.data = numpy.zeros((x, y, z))
        self._center_point = numpy.array([x // 2, y // 2, z // 2])
        self._diagonal = distance(self._center_point, numpy.array([0, 0, 0]))
        self.__marching_func = marching_cubes

    @property
    def max_value(self):
        return numpy.max(self.data)

    def iterate(self):
        for x in range(self.x):
            for y in range(self.y):
                for z in range(self.z):
                    yield x, y, z

    def normalize(self):
        self.data -= self.data.min()
        self.data /= self.data.max()

    def set_point(self, x, y, z, value):
        self.data[x, y, z] = value
        logging.debug(f'Set [{x}, {y}, {z}] = {value}')

    def get_point(self, x, y, z):
        return self.data[x, y, z]

    def distance_from_center(self, x, y, z):
        p = numpy.array([x, y, z])
        dist = self._diagonal - distance(self._center_point, p)
        normalized_dist = dist / self._diagonal
        logging.debug(f'{dist=} {normalized_dist=}')
        return normalized_dist * normalized_dist

    def apply_function(self, func):
        for x, y, z in self.iterate():
            value = func(x, y, z)
            self.set_point(x, y, z, value)

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

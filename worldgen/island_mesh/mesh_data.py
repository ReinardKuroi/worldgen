from typing import Tuple

import numpy
import logging


def distance(a: numpy.array, b: numpy.array):
    return numpy.linalg.norm(b - a)


class MeshData:
    def __init__(self, x, y, z):
        self.data = numpy.zeros((x, y, z))
        self._center_point = numpy.array([x // 2, y // 2, z // 2])
        self._diagonal = distance(self._center_point, numpy.array([0, 0, 0]))

    @property
    def max_value(self):
        return numpy.max(self.data)

    def normalize(self):
        self.data = self.data / self.max_value

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


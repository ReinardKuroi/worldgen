import numpy
import logging

import scipy.constants
from matplotlib import pyplot
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
    def max(self):
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

    def render_points(self, colormap='coolwarm'):
        fig = pyplot.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(*self.grid, c=self.data, cmap=colormap)
        ax.axis('off')
        pyplot.show()

    def march(self, **kwargs):
        return self.__marching_func(self.data, **kwargs)


class MeshData2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.data = numpy.zeros((x, y))
        self.grid = numpy.meshgrid(*(numpy.arange(s) for s in self.data.shape), indexing='ij')

    def _apply_function(self, func):
        self.data = func(self.data)

    def create_scalar_field_from_function(self, func):
        if not isinstance(func, numpy.vectorize):
            func = numpy.vectorize(func)
        return func(*self.grid)

    def set_point(self, x, y, value):
        self.data[x, y] = value

    def get_point(self, x, y):
        return self.data[x, y]

    def render_points(self, colormap='coolwarm'):
        fig = pyplot.figure()
        ax = fig.add_subplot(111)
        ax.scatter(*self.grid, c=self.data, cmap=colormap)
        ax.set_aspect('equal')
        pyplot.show()

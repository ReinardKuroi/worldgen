import numpy
import logging


class MeshData:
    def __init__(self, x, y, z):
        self.data = numpy.zeros((x, y, z))

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



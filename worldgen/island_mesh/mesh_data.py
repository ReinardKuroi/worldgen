import numpy


class MeshData:
    def __init__(self, x, y, z):
        self.data = numpy.zeros((x, y, z))

    def set_point(self, x, y, z, value):
        self.data[x, y, z] = value

    def get_point(self, x, y, z):
        return self.data[x, y, z]


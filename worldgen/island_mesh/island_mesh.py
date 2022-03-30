import random
from typing import Tuple

import numpy
from noise.perlin import SimplexNoise, TileableNoise
import logging

from worldgen.island_mesh.mesh_data import MeshData3D
from worldgen.shapes.basic import sphere


class IslandMesh:
    def __init__(self, size: Tuple[int, int, int], scale: float = .9, ocean_level: float = 0):
        self.z_depth = size[0]
        self.y_height = size[1]
        self.x_width = size[2]
        self.scale = scale
        self.ocean_level = ocean_level
        self.mesh = MeshData3D(self.x_width,
                               self.y_height,
                               self.z_depth)

    def apply_noise(self):
        logging.info('Applying basic perlin noise...')
        self.mesh.data = self.mesh.create_scalar_field_from_function(self.point_value)

    def normalize_mesh(self):
        logging.info('Normalizing vertex probability...')
        self.mesh.normalize()

    def point_value(self, x: int, y: int, z: int) -> float:
        value = self.apply_noise_on_point(x, y, z)
        # logging.debug(f'{value=}')
        # gradient = self.spherical_gradient(x, y, z)
        # gradient = self.linear_gradient(x, y, z)
        # logging.debug(f'{gradient=}')
        # value = value * gradient * (-1)
        # value = value / (gradient + 1)
        # logging.debug(f'{value=}')
        return value

    def spherical_gradient(self, x: int, y: int, z: int) -> float:
        x0 = self.x_width / 2
        y0 = self.y_height / 2
        z0 = self.z_depth / 2
        r = (x0 + y0 + z0) / 3
        return numpy.square(x - x0) + numpy.square(y - y0) + numpy.square(z - z0) - numpy.square(r)

    def apply_noise_on_point(self, x: int, y: int, z: int) -> float:
        scale: float = self.scale
        x_scaled = x / scale
        y_scaled = y / scale
        z_scaled = z / scale

        random.seed()
        noise = TileableNoise()
        noise.randomize()
        result = noise.noise3(x_scaled, y_scaled, z_scaled, repeat=self.x_width)
        return result

    def march(self):
        vertexes, faces, normals, _ = self.mesh.march(level=self.ocean_level, gradient_direction='descent')
        return vertexes, faces, normals

import random
from typing import Tuple

import noise
import numpy
from noise import pnoise2
from noise.perlin import SimplexNoise, TileableNoise
import logging

from worldgen.island_mesh.mesh_data import MeshData3D
from worldgen.shapes.basic import sphere


class IslandMesh:
    def __init__(self, size: Tuple[int, int, int], offset: Tuple[int, int, int] = (0, 0, 0), scale: float = .9, ocean_level: float = 0):
        self.z_depth = size[0]
        self.y_height = size[1]
        self.x_width = size[2]
        self.x_offset = offset[0]
        self.y_offset = offset[1]
        self.z_offset = offset[2]

        self.scale = scale
        self.ocean_level = ocean_level
        self.mesh = MeshData3D(self.x_width,
                               self.y_height,
                               self.z_depth)
        self.radius = (self.x_width + self.y_height + self.z_depth) / 12

    def apply_noise(self):
        logging.info('Applying basic perlin noise...')
        self.mesh.data = self.mesh.create_scalar_field_from_function(self.point_value)

    def apply_sphere(self):
        self.mesh.data = self.mesh.create_scalar_field_from_function(self.sphere)

    def apply_2d_noise(self):
        logging.info('Applying 2d perlin noise...')
        self.mesh.data = self.mesh.create_scalar_field_from_function(self.noise_2d)

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

    def apply_noise_on_point(self, x: int, y: int, z: int) -> float:
        scale: float = self.scale
        result = _perlin_3d((x + self.x_offset) / scale,
                            (y + self.y_offset) / scale,
                            (z + self.z_offset) / scale,
                            octaves=3)
        return result

    def noise_2d(self, x: int, y: int, z: int) -> float:
        """turn perlin2d into a 3d scalar field"""
        scale: float = self.scale
        p2d = _perlin_2d((x + self.x_offset) / scale,
                         (z + self.z_offset) / scale,
                         octaves=3)
        if p2d > 0:
            multiplier = self._gradient(x, z)
        else:
            multiplier = 1
        result = y / scale - p2d * multiplier
        return result

    def _gradient(self, x: int, z: int) -> float:
        return 1 - ((x - self.x_width / 2) ** 2 + (z - self.z_depth / 2) ** 2) / self.radius ** 2

    def march(self):
        vertexes, faces, normals, _ = self.mesh.march(level=self.ocean_level, gradient_direction='descent')
        return vertexes, faces, normals

    def sphere(self, x, y, z):
        result = self.radius**2 - ((x - self.x_width / 2) ** 2 + (y - self.y_height / 2) ** 2 + (z - self.z_depth / 2) ** 2)
        return result


def _perlin_2d(x, y, *args, **kwargs):
    return noise.pnoise2(x, y, *args, **kwargs)


def _perlin_3d(x, y, z, *args, **kwargs):
    def perlin(a, b):
        return noise.pnoise2(a, b, *args, **kwargs)

    xy = perlin(x, y)
    yz = perlin(y, z)
    xz = perlin(x, z)
    yx = perlin(y, x)
    zy = perlin(z, y)
    zx = perlin(z, x)

    return (xy + yz + xz + yx + zy + zx) / 6.0

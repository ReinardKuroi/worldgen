from typing import Tuple

import noise
import logging

import numpy

from worldgen.island_mesh.mesh_data import MeshData3D


class IslandMesh:
    def __init__(self, size: Tuple[int, int, int], offset: Tuple[int, int, int] = (0, 0, 0), scale: float = .9,
                 level: float = .5, ocean_level: float = 0, mountain_level: float = 1.,  octaves: int = 3):
        self.octaves = octaves
        self.persistence = .5
        self.lacunarity = 2.
        self.z_depth = size[0]
        self.y_height = size[1]
        self.x_width = size[2]
        self.x_offset = offset[0]
        self.y_offset = offset[1]
        self.z_offset = offset[2]

        self.scale = scale
        self.level = level
        self.ocean_level = ocean_level
        self.mountain_level = mountain_level
        self.mesh = MeshData3D(self.x_width,
                               self.y_height,
                               self.z_depth)
        self.radius = (self.x_width + self.y_height + self.z_depth) / 6
        self._sma_x = self.x_width / 2
        self._sma_y = self.y_height / 2
        self._sma_z = self.z_depth / 2

    def apply_3d_noise(self):
        logging.info('Applying basic perlin noise...')
        self.mesh.data = self.mesh.create_scalar_field_from_function(self.noise_3d)

    def apply_sphere(self):
        self.mesh.data = self.mesh.create_scalar_field_from_function(self.sphere)

    def apply_2d_noise(self):
        logging.info('Applying 2d perlin noise...')
        self.mesh.data = self.mesh.create_scalar_field_from_function(self.noise_2d)

    def apply_combined_noise(self):
        logging.info('Applying multiple perlin noise iterations...')
        self.mesh.data = self.mesh.create_scalar_field_from_function(self.noise_combined)

    def normalize_mesh(self):
        logging.info('Normalizing vertex probability...')
        self.mesh.normalize()

    def noise_combined(self, x: int, y: int, z: int) -> float:
        p3d = self.noise_3d(x, y, z)
        p2d = self.noise_2d(x, y, z)
        gradient = p2d * (1 + self.ocean_level)
        if gradient < 0:
            return -p3d * gradient
        return p3d * gradient

    def noise_3d(self, x: int, y: int, z: int) -> float:
        p3d = _perlin_3d((x + self.x_offset) / self.scale,
                         (y + self.y_offset) / self.scale,
                         (z + self.z_offset) / self.scale,
                         octaves=self.octaves,
                         persistence=self.persistence,
                         lacunarity=self.lacunarity)
        gradient = self._gradient_3d(x, y, z) * (1 + self.ocean_level)
        return (gradient - p3d)**2 - self.mountain_level

    def noise_2d(self, x: int, y: int, z: int) -> float:
        """turn perlin2d into a 3d scalar field"""
        p2d = _perlin_2d((x + self.x_offset) / self.scale,
                         (z + self.z_offset) / self.scale,
                         octaves=self.octaves,
                         persistence=self.persistence,
                         lacunarity=self.lacunarity)
        gradient = self._gradient_2d(x, z)
        zero_level = self._zero_level(y)
        return gradient - p2d + zero_level

    def _gradient_2d(self, x: int, z: int) -> float:
        return numpy.tanh((x / self._sma_x - 1)**2 + (z / self._sma_z - 1) ** 2)

    def _gradient_3d(self, x: int, y: int, z: int) -> float:
        return numpy.tanh((x / self._sma_x - 1)**2 + (y / self._sma_y - 1)**2 + (z / self._sma_z - 1) ** 2)

    def _zero_level(self, y: int) -> float:
        return y / (self.y_height * self.mountain_level) - self.ocean_level

    def march(self):
        vertexes, faces, normals, _ = self.mesh.march(level=self.level, gradient_direction='descent')
        return vertexes, faces, normals

    def sphere(self, x, y, z):
        result = self.radius ** 2 - (
                (x - self.x_width / 2) ** 2 + (y - self.y_height / 2) ** 2 + (z - self.z_depth / 2) ** 2)
        return result


def _perlin_2d(x, y, *args, **kwargs):
    return noise.pnoise2(x, y, *args, **kwargs)


def _perlin_3d(x, y, z, *args, **kwargs):
    return noise.pnoise3(x, y, z, *args, **kwargs)

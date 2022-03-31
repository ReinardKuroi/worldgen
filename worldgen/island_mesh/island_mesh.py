from typing import Tuple

import noise
import logging

from worldgen.island_mesh.mesh_data import MeshData3D


class IslandMesh:
    def __init__(self, size: Tuple[int, int, int], offset: Tuple[int, int, int] = (0, 0, 0), scale: float = .9,
                 ocean_level: float = 0):
        self.octaves = 3
        self.persistence = .5
        self.lacunarity = 2.
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

    def apply_3d_noise(self):
        logging.info('Applying basic perlin noise...')
        self.mesh.data = self.mesh.create_scalar_field_from_function(self.noise_3d)

    def apply_sphere(self):
        self.mesh.data = self.mesh.create_scalar_field_from_function(self.sphere)

    def apply_2d_noise(self):
        logging.info('Applying 2d perlin noise...')
        self.mesh.data = self.mesh.create_scalar_field_from_function(self.noise_2d)

    def normalize_mesh(self):
        logging.info('Normalizing vertex probability...')
        self.mesh.normalize()

    def noise_3d(self, x: int, y: int, z: int) -> float:
        scale: float = self.scale
        p3d = _perlin_3d((x + self.x_offset) / scale,
                         (y + self.y_offset) / scale,
                         (z + self.z_offset) / scale,
                         octaves=self.octaves,
                         persistence=self.persistence,
                         lacunarity=self.lacunarity)
        multiplier = self._gradient_3d(x, y, z)
        if p3d < 0:
            multiplier = 1
        result = p3d * multiplier
        return result

    def noise_2d(self, x: int, y: int, z: int) -> float:
        """turn perlin2d into a 3d scalar field"""
        scale: float = self.scale
        p2d = _perlin_2d((x + self.x_offset) / scale,
                         (z + self.z_offset) / scale,
                         octaves=self.octaves,
                         persistence=self.persistence,
                         lacunarity=self.lacunarity)
        multiplier = 1

        if p2d > 0:
            multiplier = self._gradient_2d(x, z)
        result = (y - self.y_height / 2) / scale - p2d * multiplier
        return result

    def _gradient_2d(self, x: int, z: int) -> float:
        return 1 - ((x - self.x_width / 2) ** 2 + (z - self.z_depth / 2) ** 2) / self.radius ** 2

    def _gradient_3d(self, x: int, y: int, z: int) -> float:
        return 1 - 2*((x - self.x_width / 2) ** 2 + (y - self.y_height / 2) ** 2 + (
                    z - self.z_depth / 2) ** 2) / self.radius ** 2

    def march(self):
        vertexes, faces, normals, _ = self.mesh.march(level=self.ocean_level, gradient_direction='descent')
        return vertexes, faces, normals

    def sphere(self, x, y, z):
        result = self.radius ** 2 - (
                (x - self.x_width / 2) ** 2 + (y - self.y_height / 2) ** 2 + (z - self.z_depth / 2) ** 2)
        return result


def _perlin_2d(x, y, *args, **kwargs):
    return noise.pnoise2(x, y, *args, **kwargs)


def _perlin_3d(x, y, z, *args, **kwargs):
    return noise.pnoise3(x, y, z, *args, **kwargs)

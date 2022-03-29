import random
from typing import Tuple

from noise.perlin import SimplexNoise, TileableNoise
import logging

from worldgen.island_mesh.mesh_data import MeshData3D


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
        self.mesh.apply_function(self.apply_noise_on_point)

    def normalize_mesh(self):
        logging.info('Normalizing vertex probability...')
        self.mesh.normalize()

    def apply_noise_on_point(self, x, y, z):
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
        vertexes, faces, normals, _ = self.mesh.march(level=self.ocean_level, gradient_direction='ascent')
        return vertexes, faces, normals

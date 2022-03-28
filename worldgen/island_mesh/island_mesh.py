import random
from typing import Tuple

from noise.perlin import SimplexNoise
import logging

from worldgen.island_mesh.mesh_data import MeshData3D


class IslandMesh:
    def __init__(self, size: Tuple[int, int, int], scale: float):
        self.z_depth = size[0]
        self.y_height = size[1]
        self.x_width = size[2]
        self.scale = scale
        self.mesh = MeshData3D(self.x_width,
                               self.y_height,
                               self.z_depth)

    def apply_noise(self):
        logging.info('Applying basic perlin noise...')
        for x in range(self.x_width):
            for y in range(self.y_height):
                for z in range(self.z_depth):
                    value = self.apply_noise_on_point(x, y, z)
                    self.mesh.set_point(x, y, z, value)

    def apply_threshold(self, threshold):
        logging.info('Applying threshold cutoff...')
        for x in range(self.x_width):
            for y in range(self.y_height):
                for z in range(self.z_depth):
                    if self.mesh.get_point(x, y, z) > threshold:
                        value = 1
                    else:
                        value = 0
                    self.mesh.set_point(x, y, z, value)

    def apply_combined_noise(self, threshold):
        logging.info('Applying fast noise...')
        for x in range(self.x_width):
            for y in range(self.y_height):
                for z in range(self.z_depth):
                    if self.apply_noise_on_point(x, y, z) * self.mesh.distance_from_center(x, y, z) > threshold:
                        self.mesh.set_point(x, y, z, 1)

    def normalize_mesh(self):
        logging.info('Normalizing vertex probability...')
        self.mesh.normalize()

    def apply_noise_on_point(self, x, y, z):
        scale: float = self.scale

        random.seed()
        noise = SimplexNoise(period=2)
        noise.randomize()
        result = noise.noise3(x * scale, y * scale, z * scale)
        return result

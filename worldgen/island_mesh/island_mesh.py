import random
from typing import Tuple
from noise import pnoise3
import logging

from worldgen.island_mesh.mesh_data import MeshData


class IslandMesh:
    def __init__(self, size: Tuple[int, int, int], scale: float):
        self.z_depth = size[0]
        self.y_height = size[1]
        self.x_width = size[2]
        self.scale = scale
        self.mesh = MeshData(self.x_width,
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

    # def normalize_mesh(self):

    def apply_noise_on_point(self, x, y, z):
        scale: float = self.scale
        octaves: int = 5
        persistence: float = .7
        lacunarity: float = 1.5

        random.seed()
        global_random_offset_x = random.randint(0, 1024 * 1024)
        global_random_offset_y = random.randint(0, 1024 * 1024)
        global_random_offset_z = random.randint(0, 1024 * 1024)

        result = pnoise3((x + global_random_offset_x) * scale,
                         (y + global_random_offset_y) * scale,
                         (z + global_random_offset_z) * scale,
                         octaves=octaves,
                         persistence=persistence,
                         lacunarity=lacunarity,
                         repeatx=self.x_width,
                         repeaty=self.y_height,
                         repeatz=self.z_depth,
                         base=0)
        return result

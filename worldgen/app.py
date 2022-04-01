import logging
import subprocess
from datetime import datetime

from matplotlib import pyplot, cm
import random
import noise
import numpy

from worldgen.island_mesh.island_mesh_factory import IslandMeshFactory
from worldgen.object.mesh import MeshObject


def generate_heightmap(x_width, y_height, world):
    scale: float = 256
    octaves: int = 5
    persistence: float = .7
    lacunarity: float = 1.5

    random.seed()
    global_random_offset_x = random.randint(0, 1024 * 1024)
    global_random_offset_y = random.randint(0, 1024 * 1024)

    for x in range(x_width):
        for y in range(y_height):
            world[x][y] = noise.pnoise2((x + global_random_offset_x) / scale, (y + global_random_offset_y) / scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=x_width,
                                        repeaty=y_height,
                                        base=0)
    return world


def visualize(data):
    pyplot.imshow(data)
    pyplot.axis('off')
    pyplot.show()


def visualize3d(data):
    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    x, y = numpy.meshgrid(range(data.shape[0]), range(data.shape[1]))
    ax.plot_surface(x, y, data, cmap=cm.terrain)
    ax.set_axis_off()
    ax.set_zlim(0, 7)
    pyplot.show()


def visualize_voxels(data):
    fig = pyplot.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(data, edgecolors='k', facecolors='blue')
    ax.axis('off')
    pyplot.show()


def random_offset():
    import random
    random.seed()
    x = random.random() * 2 ** 12
    y = random.random() * 2 ** 12
    z = random.random() * 2 ** 12
    return x, y, z


def main():
    tree_growth_range: (float, float)
    island_size: float = .4
    island_complexity: float = 5
    ocean_level: float = .47
    mountain_level: float = .7
    resolution = 8
    xyz = (1024//resolution, 512//resolution, 1024//resolution)
    offset = random_offset()
    scale: float = 256//resolution

    """
        Generate some sort of noise map for the island shape
        This will produce a 2 dimensional matrix with values 0..1
        Based on the matrix content and filters, we can create a 2d island
        Afterwards we can populate the island using additional noise layers
        To make it 3d it is possible to add another noise iteration, this time inverted
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    island_factory = IslandMeshFactory(xyz, offset=offset, scale=scale, level=island_size, ocean_level=ocean_level,
                                       mountain_level=mountain_level, octaves=island_complexity)
    time_start = datetime.now()
    island = island_factory.new()
    time_init = datetime.now()
    island.apply_combined_noise()
    island.normalize_mesh()
    time_gen = datetime.now()
    mesh_object = MeshObject(*island.march())
    time_end = datetime.now()
    logging.info(f'Total time: {time_end - time_start}')
    logging.info(f'Init: {time_init - time_start}')
    logging.info(f'Generation time: {time_gen - time_init}')
    logging.info(f'Render time: {time_end - time_gen}')
    file = mesh_object.save_as_obj()
    # subprocess.run('C:\Program Files\VCG\MeshLab\meshlab.exe ' + file)

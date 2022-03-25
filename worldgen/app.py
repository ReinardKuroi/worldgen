import logging

from matplotlib import pyplot, cm
import random
import noise
import numpy

from worldgen.island_mesh.island_mesh_factory import IslandMeshFactory


def generate_heightmap(x_width, y_height, world):
    scale: float = 256
    octaves: int = 5
    persistence: float = .7
    lacunarity: float = 1.5

    random.seed()
    global_random_offset_x = random.randint(0, 1024*1024)
    global_random_offset_y = random.randint(0, 1024*1024)

    for x in range(x_width):
        for y in range(y_height):
            world[x][y] = noise.pnoise2((x + global_random_offset_x)/scale, (y + global_random_offset_y)/scale,
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


def visualize_points(data):
    fig = pyplot.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(*data.nonzero())
    ax.axis('off')
    pyplot.show()


def filter_cutoff(x_width, y_height, world, ground_zero):
    ocean = [0, .1]
    beach = [.1, .15]
    plains = [.15, .25]
    mountains = [.25, 1]
    world = world/numpy.max(world)
    for x in range(x_width):
        for y in range(y_height):
            z = world[x][y]
            if z in ocean:
                world[x][y] = 0
            if z in beach:
                world[x][y] = .1
            if z in plains:
                world[x][y] = .15
            if z in mountains:
                world[x][y] = .25
            # if world[x][y] < ground_zero:
            #     world[x][y] = None
    return world


def render_map(filtered_heightmap):
    pass


def main():
    ocean_level: float = .2
    tree_growth_range: (float, float)
    island_size: float
    island_complexity: float

    x_width: int = 256
    y_height: int = 256
    z_depth: int = 256
    scale: float = .01

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

    island_factory = IslandMeshFactory()
    island = island_factory.new((x_width, y_height, z_depth), scale)
    # island.apply_noise()
    # island.apply_threshold(.45)
    island.apply_combined_noise(.8)

    # heightmap = generate_heightmap(x_width, y_height, empty_world)
    # heightmap = filter_cutoff(x_width, y_height, heightmap, ocean_level)
    # print(island.mesh.data)
    visualize_points(island.mesh.data)
    #
    # visualize(filtered_heightmap)
    # island = render_map(filtered_heightmap)

    

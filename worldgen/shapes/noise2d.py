import cProfile
import functools
import timeit
from functools import reduce

import noise
import numpy
from matplotlib import pyplot

permutation = (151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36,
               103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148, 247, 120, 234, 75, 0,
               26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33, 88, 237, 149, 56,
               87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166,
               77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55,
               46, 245, 40, 244, 102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132,
               187, 208, 89, 18, 169, 200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109,
               198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126,
               255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183,
               170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43,
               172, 9, 129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112,
               104, 218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162,
               241, 81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106,
               157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205,
               93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180)

p = permutation * 2

sqrt_2 = numpy.sqrt(2)

grad2d = numpy.array(
    [[1, 1],
     [-1, 1],
     [1, -1],
     [-1, -1],
     [sqrt_2, 0],
     [0, sqrt_2],
     [0 - sqrt_2, 0],
     [0, 0 - sqrt_2]]
) / sqrt_2

square = numpy.array(
    [[0, 0],
     [0, 1],
     [1, 0],
     [1, 1]]
)


@numpy.vectorize
def dot_grad(v, hash):
    numpy.dot(v, grad(hash))


@numpy.vectorize
def fade(v: numpy.ndarray):
    return 6 * v ** 5 - 15 * v ** 4 + 10 * v ** 3


@numpy.vectorize
def lerp(t: numpy.ndarray, a: numpy.ndarray, b: numpy.ndarray):
    return a + t * (b - a)


@numpy.vectorize
def grad(h: int):
    return grad2d[h]


@numpy.vectorize
def hash2d(x, y) -> int:
    return p[p[x] + y]


@numpy.vectorize
def hash3d(x, y, z) -> int:
    return p[p[p[x] + y] + z]


@numpy.vectorize
def ndhash(*v) -> int:
    if len(v) > 1:
        return p[ndhash(*v[1:]) + v[0] & 255]
    else:
        return p[v[0] & 255]


def hashgrad2d(x, y):
    return grad2d[p[p[x] + y] & 7]


with cProfile.Profile() as pr:
    offset = (0, 0)
    shape = (1000, 1000)
    scale = (6, 6)
    """
    expand grid of 0-10, 0-10 to 0 0 0 0 .... 9 9 9 9 10
    create 4 grids with offsets
    dot each with input.
    """

    points = numpy.meshgrid(*((numpy.arange(0, s * x, x) / s) + o for o, s, x in zip(offset, shape, scale)), indexing='ij')
    point_space = numpy.dstack(points)
    relative_point_space = numpy.floor(point_space)

    grid = numpy.int_(numpy.meshgrid(*(numpy.arange(o, s + o) * x // s for o, s, x in zip(offset, shape, scale)), indexing='ij'))

    # multigrad = [grad2d[ndhash(numpy.apply_along_axis(lambda x: x + v, -1, numpy.dstack(grid))) & 7].reshape(*shape, 2) for v in square]

    g00 = hashgrad2d(*grid)
    p00 = point_space - relative_point_space
    # g01 = grad2d[ndhash(*grid) & 7]
    result = numpy.sum(p00 * g00, axis=2)

    ######################

    # input_grid = numpy.meshgrid(*(numpy.arange(s * x) / x for s, x in zip(shape, scale)), indexing='ij')
    # input_vectors = numpy.dstack(input_grid)
    #
    # grid = numpy.meshgrid(*(numpy.arange(start=o, stop=o+s+1) for o, s, x in zip(offset, shape, scale)), indexing='ij')
    # global_hash_table = ndhash(*grid) & 7
    # local_grid = numpy.meshgrid(*(numpy.arange(start=o, stop=o+s*x) for o, s, x in zip(offset, shape, scale)), indexing='ij')
    # local_hash_table = ndhash(*numpy.int_(input_grid)) & 7
    # idx_vectors = numpy.dstack(grid)
    # grad_table = grad2d[global_hash_table].reshape(*shape, 2)
    #
    # data = input_vectors.floor
    # numpy.sum(random_data * grad_table, axis=2)
    # gdx, gdy = grad(global_hash_table)
pr.print_stats(sort='tottime')
pyplot.imshow(result)


@numpy.vectorize
def perlin2d(v: numpy.ndarray) -> float:
    v_rel = square + numpy.floor(v) - v
    v_fade = fade(-v_rel[0])
    v_idx = square + numpy.int_(v) & 255
    v_hash = numpy.apply_along_axis(hash2d, 1, v_idx)
    v_grad = grad(v_hash)
    v_dot = numpy.einsum('ij,ij->i', v_rel, v_grad).reshape(2, 2)
    v_lerp = lerp(v_fade[0], *lerp(v_fade[1], *v_dot))
    return v_lerp


@numpy.vectorize
def gradient_grid(shape):
    grid = numpy.meshgrid(*(numpy.arange(x) for x in shape), indexing='ij')
    v_hash = hash2d(*grid) & 7
    v_grad = grad(v_hash)
    return v_grad


@numpy.vectorize
def perlin2d_wrapper(x, y) -> float:
    scale = 10
    return perlin2d(numpy.array([x, y], dtype=float) / scale)


@numpy.vectorize
def pnoise2_wrapper(x, y) -> float:
    scale = 10
    return noise.pnoise2(x / scale, y / scale)


grid = numpy.meshgrid(*(numpy.arange(x) for x in (256, 256)), indexing='ij')
# data = perlin2d(grid)
fig = pyplot.figure()
ax = fig.add_subplot(111)
gd = numpy.dstack((gdx, gdy))
ax.quiver(*gd, cmap='coolwarm')
ax.set_aspect('equal')
pyplot.show()

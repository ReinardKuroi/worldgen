import numpy


def random_cube():
    return numpy.random.randint(low=0, high=2, size=(2, 2, 2))


def iterate_as_cube_data(data: numpy.ndarray) -> numpy.ndarray:
    for x in range(data.size):
        yield random_cube()


def check_hash(cube, cube_hash):
    check = int(''.join([str(s) for s in reversed(cube.flatten())]), 2)
    assert check == cube_hash, f'{check} != {cube_hash}'


def calculate_hash(cube: numpy.ndarray):
    cube_hash = 0
    for i, v in enumerate(cube.flat):
        if v == 1:
            cube_hash += 1 << i
    check_hash(cube, cube_hash)
    return cube_hash


def march(data: numpy.ndarray):
    for cube in iterate_as_cube_data(data):
        cube_hash = calculate_hash(cube)
        print(f'{cube.flatten()} hash: {cube_hash}')


march(numpy.zeros((128*128,)))

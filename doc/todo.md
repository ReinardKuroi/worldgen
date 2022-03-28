# TODO

## Basic ideas

- floating islands
- 3d
- props (trees houses rocks)
- the bottom part of the floating island
- maybe like cave entrances on the side
- spinning camera for preview

## Technical babble

- separate data generation from rendering
- come up with lightweight rendering system
- possibility to export object files
- separate functions for generation
- possibility to export heightmaps for future use

## Usefull stuff

- perlin2d for maps _hold thath thought_
- ~~perlin3d for caves~~ simplex3D is faster (O(n^2) vs O(2^N))
- triplanar mapping?

## Problems

### Speed

The generation is tediously slow since it is basically O(n^3).
Might want to look into GPU utilization.

- currently using numpy.array((x, y, z))
- iterating over with `for coord in coord_dimension:` nested
- time to compute is O(n^3)
- maybe can apply function to matrix with numpy

### Data representation

How to efficiently represent vertex data and manipulate it? Look into python matrices.
- try [`pointcloud`](https://pointclouds.org/)
- ~~matplotlib voxels~~ too heavy for rendering alhough cute
- 3d array to .obj using marching cubes which by the way also allows using intermediate values other than 0 and 1

There must be a way to better represent 3 meshes than a 2d array with floats.

### Transforming 3D array into .obj

Manually serializing vertex and face data to text works fine.
Problem is the 3d array to vertex data transform doesn't work properly.

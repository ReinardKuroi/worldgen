# TODO

## Basic ideas

- [x] floating islands
- [x] 3d
- [ ] props (trees houses rocks)
- [x] the bottom part of the floating island
- [ ] maybe like cave entrances on the side
- [ ] spinning camera for preview
- [ ] correct orientation for Blender/Unreal/Unity
- [ ] add CLI for params used in app.py

## Technical babble

- [ ] separate data generation from rendering
- [x] come up with lightweight rendering system - **MeshLab**
- [x] possibility to export object files
- [ ] separate functions for generation
- [ ] possibility to export heightmaps for future use
- [ ] smooth normals
- [ ] implement `perlin2d` using `numpy`
- [ ] implement `perlin2d` using `numpy`
- [ ] generic surface generation with `numpy`

## Usefull stuff

- perlin2d for maps _hold that thought_
- ~~perlin3d for caves~~ simplex3D is faster (O(n^2) vs O(2^N))
- triplanar mapping?
- combine 2d perlin and 3d perlin for 3d islands

## Problems

### Speed

The generation is tediously slow since it is basically O(n^3).
Might want to look into GPU utilization.

- currently using numpy.array((x, y, z))
- ~~iterating over with `for coord in coord_dimension:` nested~~
- time to compute is O(n^3)
- maybe can apply function to matrix with numpy
- scalar operations are **slow**

**Solution:**
`numpy` allows efficient scalar field computing, have to optimize functions to use vector operations though.

### Data representation

How to efficiently represent vertex data and manipulate it? Look into python matrices.
- ~~try pointcloud~~
- ~~matplotlib voxels~~ too heavy for rendering alhough cute
- ~~3d array to .obj using marching cubes which by the way also allows using intermediate values other than 0 and 1~~

~~There must be a way to better represent 3 meshes than a 2d array with floats.~~

**Solution:**
`3d meshgrid` for coordinates, `3d scalar field` for mesh point data - allows to apply matrix operations to xyz data and return a scalar field. 

### Transforming 3D array into .obj

Manually serializing vertex and face data to text works fine.
~~Problem is the 3d array to vertex data transform doesn't work properly.~~

**Solution:**

- vertex: `v x y z`
- face: `f f vx_id vy_id vz_id`

```
v 0 0 0
v 0 1 0
v 0 0 1
v 1 0 0

f 1 3 2
f 1 2 4
f 1 4 3
f 2 3 4
```

# Plans

Easiest way is to have a high-level aggregator class `IslandMesh` that combines multiple transformation methods.

`IslandMesh` should provide a property to access its mesh data in whatever form.
It also keeps data on additional props and textures.
`MeshData` keeps mesh data and implements methods necessary to transform this mesh.
`IslandMeshFactory` provides an interface for generating new islands.
`MeshObject` is responsible for data -> .obj transformation.

On an abstract level, island is generated in a few steps:

- a blank mesh is created that we will modify
  - this heavily depends on the way we are going to keep the data
  - this also can be separated into multiple steps if the surface data is broken up into multiple parts
- basic deformations are applied (heightmap)
- additional deformations are applied (caves and rivers)
- mesh then can be exported and rendered

- additional object maps are created to populate the island with different props

Instead of using pyplot to generate meshes, combine marching cubes and .obj export to create 3d models.

To speed things up, instead of creating multiple scalar fields and combining them,
it is faster to create a single function that describes point values at `[x, y, z]`.
This function can use mathematical and logical operations to determine the value `p0(x0, y0, z0)`.
This way we only iterate over the space once and produce a final result. Some functions,
e.g. normalizing values using a sigmoid, are fast enough to be applied afterwards.

Mainland generation is based on a single function `f(x, y, z)` that provides a value
for each point `p(px, py, pz)`. It is preferred to keep those values in range `(-1, 1)` but since we
normalize by using an exponential logistic function,
the resulting shape is described by values in range `(0, 1)`.

Since we are generating a discrete scalar field with a fixed step of `1`,
it is fastest to start with a `grid: numpy.meshgrid` with shape `(x_max, y_max, z_max)`.
By applying a function to vector `[x, y, z]`, we get a resulting value `v` for each point in this grid.
This way, we create a scalar field `data: numpy.ndarray = numpy.zeros((x_max, y_max, z_max))`
and apply function `f()` to `[grid_x, grid_y, grid_z]` and populate `data[x, y, z]` with `f(x, y, z)`.

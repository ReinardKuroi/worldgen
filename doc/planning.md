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

Using pyplot for visualization has some problems. Have to figure out something to generate meshes.
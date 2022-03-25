from worldgen.island_mesh.island_mesh import IslandMesh


class IslandMeshFactory:
    def __init__(self):
        self.__factory = IslandMesh

    def new(self, size=(256, 256, 256), scale=.1):
        return self.__factory(size=size, scale=scale)

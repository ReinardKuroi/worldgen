from worldgen.island_mesh.island_mesh import IslandMesh


class IslandMeshFactory:
    def __init__(self):
        self.__factory = IslandMesh

    def new(self, *args, **kwargs):
        return self.__factory(*args, **kwargs)

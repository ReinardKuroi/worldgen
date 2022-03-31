from worldgen.island_mesh.island_mesh import IslandMesh


class IslandMeshFactory:
    def __init__(self, *args, **kwargs):
        self.__factory = IslandMesh
        self.args = args
        self.kwargs = kwargs

    def new(self, *args, **kwargs):
        return self.__factory(*self.args, *args, **self.kwargs, **kwargs)

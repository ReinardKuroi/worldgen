from datetime import datetime

from matplotlib import pyplot
from skimage.measure import marching_cubes


from worldgen.island_mesh.mesh_data import MeshData


class MeshObject:
    def __init__(self, mesh_data: MeshData):
        vertexes, faces, normals, values = marching_cubes(mesh_data.data, 0)
        self.vertexes = vertexes
        self.faces = faces
        self.normals = normals
        self.values = values

    def save_as_obj(self, filename=None):
        if not filename:
            filename = 'island' + datetime.now().strftime('%d%m%y_%H%M%S') + '.obj'
        with open(filename, 'w') as f:
            f.write(f'Mesh o\n')
            for vertex in self.vertexes:
                f.write(f'v {vertex[0]} {vertex[1]} {vertex[2]}\n')
            for normal in self.normals:
                f.write(f'vn {normal[0]} {normal[1]} {normal[2]}\n')
            for face in self.faces:
                f.write(f'f {face[0]}/{face[0]} {face[1]}/{face[1]} {face[2]}/{face[2]}\n')

    def render(self):
        fig = pyplot.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot_trisurf(self.vertexes[:, 0], self.vertexes[:, 1], self.faces, self.vertexes[:, 2], linewidth=.2)
        ax.axis('off')
        pyplot.show()

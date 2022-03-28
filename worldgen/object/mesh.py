from datetime import datetime

from matplotlib import pyplot
from skimage.measure import marching_cubes

from worldgen.island_mesh.mesh_data import MeshData3D


class MeshObject:
    def __init__(self, mesh_data: MeshData3D):
        vertexes, faces, normals, values = self.generate_mesh(mesh_data.data)
        self.vertexes = vertexes
        self.faces = faces
        self.normals = normals
        self.values = values

    def save_as_obj(self, filename=None):
        if not filename:
            filename = 'island' + datetime.now().strftime('%d%m%y_%H%M%S') + '.obj'
        with open(filename, 'w') as f:
            f.write(f'Mesh o\n')
            f.writelines(map(self.vertex_to_str, self.vertexes))
            f.writelines(map(self.normal_to_str, self.normals))
            f.writelines(map(self.face_to_str, self.faces))

    @staticmethod
    def vertex_to_str(vertex):
        return f'v {vertex[0]} {vertex[1]} {vertex[2]}\n'

    @staticmethod
    def normal_to_str(normal):
        return f'vn {normal[0]} {normal[1]} {normal[2]}\n'

    def vertex_for_face_to_str(self, index):
        vertex = self.vertexes[index]
        return f'{vertex[0]}/{vertex[1]}/{vertex[2]}'

    def face_to_str(self, face):
        return f'f {face[0]} {face[1]} {face[2]} \n'
        # return (f'f {self.vertex_for_face_to_str(face[0])} '
        #         f'{self.vertex_for_face_to_str(face[1])} '
        #         f'{self.vertex_for_face_to_str(face[2])}\n')

    def render(self):
        fig = pyplot.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot_trisurf(self.vertexes[:, 0], self.vertexes[:, 1], self.faces, self.vertexes[:, 2], linewidth=.2)
        ax.axis('off')
        pyplot.show()

    def generate_mesh(self, data):
        return marching_cubes(data, 0)

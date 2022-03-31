import logging
from datetime import datetime

from matplotlib import pyplot


class MeshObject:
    def __init__(self, vertexes, faces, normals, *args):
        self.vertexes = vertexes
        self.faces = faces
        self.normals = normals

    def save_as_obj(self, filename=None):
        if not filename:
            filename = 'island' + datetime.now().strftime('%d%m%y_%H%M%S') + '.obj'
        logging.info(f'Saving as {filename}')
        with open(filename, 'w') as f:
            f.writelines(map(self.vertex_to_str, self.vertexes))
            f.writelines(map(self.normal_to_str, self.normals))
            f.writelines(map(self.face_to_str, self.faces + 1))
        return filename

    @staticmethod
    def vertex_to_str(vertex):
        return f'v {vertex[0]} {vertex[1]} {vertex[2]}\n'

    @staticmethod
    def normal_to_str(normal):
        return f'vn {normal[0]} {normal[1]} {normal[2]}\n'

    @staticmethod
    def face_to_str(face):
        return f'f {face[0]} {face[1]} {face[2]} \n'

    def render(self):
        fig = pyplot.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot_trisurf(self.vertexes[:, 0], self.vertexes[:, 1], self.faces, self.vertexes[:, 2], linewidth=.2)
        ax.axis('off')
        pyplot.show()

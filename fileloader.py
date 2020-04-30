import OpenGL.GL as gl
import numpy as np

from geometry.vec3 import Vec3
from geometry.face import Face
from geometry.materials import Materials as mtl


class ObjLoader:
    def __init__(self, fileName):
        self.vertices = np.empty((0), dtype=Vec3)
        self.normals = np.empty((0), dtype=Vec3)
        self.faces = np.empty((0), dtype=Face)

        # Parse file and construct list of vertices, faces, and face normals
        try:
            file = open(fileName)
            for line in file:
                if line.startswith("v "):
                    line = line.strip().split()
                    vertex = Vec3(line[1], line[2], line[3])

                    self.vertices = np.append(self.vertices, vertex)

                elif line.startswith("vn"):
                    line = line.strip().split()
                    normal = Vec3(line[1], line[2], line[3])

                    self.normals = np.append(self.normals, normal)

                elif line.startswith("f"):
                    if "/" in line:
                        line = line.strip().split()
                        faceData = [
                            line[1].split("/"),
                            line[2].split("/"),
                            line[3].split("/"),
                        ]
                        vertRef = [
                            int(faceData[0][0]),
                            int(faceData[1][0]),
                            int(faceData[2][0]),
                        ]
                        vertices = np.array(
                            [
                                self.vertices[vertRef[0] - 1],
                                self.vertices[vertRef[1] - 1],
                                self.vertices[vertRef[2] - 1],
                            ]
                        )
                        # Calculate face normal using vertex normals
                        faceNorm = None
                        if len(self.normals) > 0:
                            faceNorm = (
                                np.sum(
                                    np.array(
                                        [
                                            self.normals[int(faceData[0][2]) - 1].vec,
                                            self.normals[int(faceData[1][2]) - 1].vec,
                                            self.normals[int(faceData[2][2]) - 1].vec,
                                        ],
                                        dtype=float,
                                    ),
                                    axis=0,
                                )
                                / 3
                            )
                            faceNorm = Vec3(*(-faceNorm))
                    else:
                        line = line.strip().split()
                        vertices = (int(line[1]), int(line[2]), int(line[3]))
                        faceNorm = Vec3(0, 0, 0)

                    self.faces = np.append(self.faces, Face(vertices, faceNorm))

            file.close()
        except IOError:
            print(".obj file not found.")

    def render(self, material_view=False):
        """
        Returns renderable call list of vertices representing the model.
        """
        if material_view:
            polygon_mode = gl.GL_FILL
        else:
            polygon_mode = gl.GL_LINE

        if len(self.faces) > 0:
            gl_list = gl.glGenLists(1)
            gl.glNewList(gl_list, gl.GL_COMPILE)
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, polygon_mode)
            gl.glBegin(gl.GL_TRIANGLES)
            for face in self.faces:
                for vertex in face.vertices:
                    vertexDraw = vertex.vec
                    gl.glColor4fv(mtl.color(face.material))
                    gl.glVertex3fv(vertexDraw)
            gl.glEnd()
            gl.glEndList()
        return gl_list

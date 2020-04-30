import numpy as np
from geometry.vec3 import Vec3


def volume(vertices, faces):
    """
    Calculates volume of the object denoted by the given vertices
    and faces using triangulation
    """
    vols = []
    for face in faces:
        vols = np.append(
            vols,
            signed_volume_triangle(
                face.vertices[0], face.vertices[1], face.vertices[2]
            ),
        )
    return np.abs(np.sum(vols))


def signed_volume_triangle(v1: Vec3, v2: Vec3, v3: Vec3):
    """
    Calculates the signed volume of a triangle through its relation
    to the origin as a tetrahedron
    """
    return v1.dot(v2.cross(v3)) / 6.0


def surface_area(faces):
    """
    Calculates surface area of the object denoted by the given vertices
    and faces using triangulation
    """
    area = []
    for face in faces:
        area.append(triangle_area(face.vertices[0], face.vertices[1], face.vertices[2]))
    return np.sum(area)


def triangle_area(v1, v2, v3):
    """
    Calculates the area of a triangle using its vertices
    """
    return 0.5 * np.linalg.norm(np.cross(v2.vec - v1.vec, v3.vec - v1.vec))


def calc_center(vertices, faces):
    """
    Calculates center of the object denoted by the given vertices
    and faces using triangulation
    """
    centers = []
    for face in faces:
        centers.append(
            triangle_center(face.vertices[0], face.vertices[1], face.vertices[2])
        )
    return Vec3(*np.mean(centers, axis=0))


def triangle_center(v1, v2, v3):
    """
    Calculates the center of a triangle
    """
    return np.mean([v1.vec, v2.vec, v3.vec], axis=0)

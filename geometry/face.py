import numpy as np

from geometry.vec3 import Vec3
from formulas.geometric_formulas import triangle_area
from geometry.materials import Materials as mtl


class Face:
    """
    Represents the triangular face of a 3D object
    """

    def __init__(
        self,
        vertices: np.ndarray,
        normal: Vec3 = None,
        kd: float = 0.1,
        ks: float = 0.9,
        material: int = mtl.HARDWOOD,
    ):
        self.vertices = vertices
        if normal is not None:
            self.normal = normal
        elif len(vertices) >= 3:
            self.normal = self.calc_normal()
        self.edge1 = self.vertices[1].sub(self.vertices[0])
        self.edge2 = self.vertices[2].sub(self.vertices[0])
        self.kd = kd
        self.ks = ks
        self.surface_area = triangle_area(*self.vertices)
        self.material = material

    def __str__(self):
        """
        Provides a useful string representation of a Face object. 
        """
        string = "Vertices: ["
        for v in self.vertices:
            string += v.__str__()
        string += "] Face Normal: " + self.normal.__str__()
        string += " Material: " + mtl.name(self.material)
        return string

    def calc_normal(self):
        """
        Calculate the face normal using the vertices
        """
        normal = np.cross(
            self.vertices[1].vec - self.vertices[0].vec,
            self.vertices[2].vec - self.vertices[0].vec,
        )
        return Vec3(*normal).normalize()

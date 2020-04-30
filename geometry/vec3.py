import math
import numpy as np


class Vec3:
    """
    An enhanced tuple containing 3 points
    """

    def __init__(self, x: float, y: float, z: float):
        self.vec = np.array([x, y, z], dtype=float)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        """
        Provides a useful string representation of a Vec3 object.
        """
        return self.vec.__str__()

    def __iter__(self):
        """
        Vec3 iterator.
        """
        self.num = 0
        return self

    def __next__(self):
        """
        Vec3 next function for iteration.
        """
        if self.num >= 3:
            raise StopIteration

        self.num += 1
        if self.num == 1:
            return self.x
        elif self.num == 2:
            return self.y
        else:
            return self.z

    def __neg__(self):
        """
        For negating Vec3 objects.
        """
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, other: float):
        """
        For scalar multiplication of a Vec3 object by a float.
        """
        return Vec3(self.x * other, self.y * other, self.z * other)

    def add(self, v: "Vec3"):
        """
        Adds 2 Vec3 objects together
        """
        return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def sub(self, v: "Vec3"):
        """
        Subtracts 2 Vec3 objects together
        """
        return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)

    def dot(self, v: "Vec3"):
        """
        Calculates the dot product of 2 Vec3 objects
        """
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v: "Vec3"):
        """
        Calculates the cross product of 2 Vec3 objects
        """
        return Vec3(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x,
        )

    def length(self):
        """
        Calculates the length of the Vec3 object
        """
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        """
        Normalizes the Vec3 object
        """
        l = self.length()
        return Vec3(self.x / l, self.y / l, self.z / l)

    def sq_distance(self, other: "Vec3"):
        """
        Calculates the squared distance between 2 vertices
        """
        dx = (self.x - other.x) ** 2
        dy = (self.y - other.y) ** 2
        dz = (self.z - other.z) ** 2
        return dx + dy + dz

    def distance(self, other: "Vec3"):
        """
        Calculates the distance between 2 vertices
        """
        return math.sqrt(self.sq_distance(other))

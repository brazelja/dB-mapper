from geometry.vec3 import Vec3
from geometry.materials import Materials as mtl


class Ray:
    def __init__(
        self,
        origin: Vec3,
        direction: Vec3,
        dist_from_origin: float = None,
        db: float = None,
    ):
        self.origin = origin
        self.direction = direction
        self.dist_from_origin = dist_from_origin
        self.start_db = db

    def __str__(self) -> str:
        """
        Provides a useful string representation of a Ray object.
        """
        return (
            "Origin: "
            + self.origin.__str__()
            + " Direction: "
            + self.direction.__str__()
        )

    def calc_reflection(self, phit, normal, dist_from_origin, db) -> "Ray":
        """
        Calculates the reflected Ray based on incidence and normal
        """
        ray = Vec3(*(-(normal * (self.direction.dot(normal) * 2)).sub(self.direction)))
        return Ray(phit, ray, dist_from_origin, db)

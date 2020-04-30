import random
import math
import numpy as np
from geometry.vec3 import Vec3
from geometry.face import Face
from geometry.ray import Ray


def generate_brdf(
    sm: Ray, phit: Vec3, start_db: float, dist_from_origin: float, face: Face
):
    """
    Generates an array of rays whose starting dB levels are calculated using the Phong BRDF model
    ## D( kd( Sm.dot(normal) ) + ks( V.dot(Rm) ) )
    - D  - the percentage of acoustic energy in each ray\n
    - kd - diffusion coefficient\n
    - ks - specular coefficient\n
    - Sm - incident ray\n
    - n  - surface normal\n
    - V  - reflected ray\n
    - Rm - rays of hemisphere from surface
    """
    rm = sm.calc_reflection(phit, face.normal, dist_from_origin, start_db)
    v = generate_v(
        phit,
        face.normal,
        face.normal.dot(rm.direction),
        start_db,
        dist_from_origin,
        100,
    )
    diffuse = face.kd * sm.direction.dot(face.normal)
    for ray in v:
        specular = face.ks * rm.direction.dot(ray.direction)
        ray.start_db = start_db * (diffuse + specular)

    v = [rm] + v
    return v


def generate_v(
    origin: Vec3,
    normal: Vec3,
    valid_side: float,
    start_db: float,
    dist_from_origin: float,
    ray_num,
) -> list:
    """
    Generates rays in a hemisphere to represent reflected rays 
    """
    rnd = random.random() * ray_num

    points = []
    offset = 2.0 / ray_num
    increment = math.pi * (3.0 - math.sqrt(5.0))

    for i in range(ray_num):
        y = ((i * offset) - 1) + (offset / 2)
        r = math.sqrt(1 - pow(y, 2))

        phi = ((i + rnd) % ray_num) * increment

        x = math.cos(phi) * r
        z = math.sin(phi) * r

        vec = Vec3(x, y, z).normalize()
        if np.sign(normal.dot(vec)) != np.sign(valid_side):
            # Ensure that the rays are inside the object
            vec = -vec
        points.append(Ray(origin, vec, dist_from_origin, start_db))
    return points

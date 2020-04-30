import math
from colorsys import hsv_to_rgb
from geometry.materials import Materials as mtl


def drop_off(dist_1, dist_2):
    """
    Calculates the decibel level change between two distances
    """
    if dist_1 <= 0 or dist_2 <= 0:
        raise Exception("Distances from source cannot be 0")

    db_change = 20 * math.log10(dist_2 / dist_1)
    return db_change


def sum_levels(levels):
    """
    Sums multiple sound levels
    """
    if len(levels) == 0:
        return 0

    sum_level = 0.0
    for level in levels:
        if level > 0:
            sum_level += math.pow(10, float(level) / 10)

    return 10 * math.log10(sum_level) if sum_level > 0 else 0


def rt60(volume, faces) -> float:
    """
    Reverberation time of the room denoted by the given faces\n
    """
    a_sum = 0
    for face in faces:
        a_sum += face.surface_area * mtl.absorption(face.material, 1000)
    reverb = 0.161 * (volume / a_sum)

    return reverb


def crit_dist(volume, faces):
    """
    Critical distance from the sound source
    - Volume is in cubic meters
    """
    reverb = rt60(volume, faces)
    critical = 0.057 * math.sqrt(volume / reverb)
    return critical


def db_to_color(level):
    """
    Converts given dB level (0-120) to RGB using HSV values
    - Range from Red to Cyan 
    - Red  ( >= 120dB ) = (0, 1, 1) HSV
    - Cyan ( <=   0dB ) = (180, 1, 1)  HSV
    """

    # Ensure level is in proper bounds
    level = 0 if level < 0 else level
    level = 120 if level > 120 else level

    hue = (level - 120) * -1.5  # HSV Hue
    return hsv_to_rgb(hue / 360, 1, 1)

class Units:
    """
    Enum variables for measurement units.
    """

    INCHES = 1
    FEET = 2
    CENTIMETERS = 3
    METERS = 4


def toInches(value, unit):
    """
    Converts the given value in its given unit to inches.
    """
    newValue = 0.0

    if unit == Units.INCHES:
        newValue = value
    elif unit == Units.FEET:
        newValue = value * 12
    elif unit == Units.CENTIMETERS:
        newValue = value / 2.54
    elif unit == Units.METERS:
        newValue = value * 39.37
    else:
        newValue = -1

    return newValue


def toFeet(value, unit):
    """
    Converts the given value in its given unit to feet.
    """
    newValue = 0.0

    if unit == Units.INCHES:
        newValue = value / 12
    elif unit == Units.FEET:
        newValue = value
    elif unit == Units.CENTIMETERS:
        newValue = value / 30.48
    elif unit == Units.METERS:
        newValue = value * 3.281
    else:
        newValue = -1

    return newValue


def toCentimeters(value, unit):
    """
    Converts the given value in its given unit to centimeters.
    """
    newValue = 0.0

    if unit == Units.INCHES:
        newValue = value * 2.54
    elif unit == Units.FEET:
        newValue = value * 30.48
    elif unit == Units.CENTIMETERS:
        newValue = value
    elif unit == Units.METERS:
        newValue = value * 100
    else:
        newValue = -1

    return newValue


def toMeters(value, unit):
    """
    Converts the given value in its given unit to meters.
    """
    newValue = 0.0

    if unit == Units.INCHES:
        newValue = value / 39.37
    elif unit == Units.FEET:
        newValue = value / 3.281
    elif unit == Units.CENTIMETERS:
        newValue = value / 100
    elif unit == Units.METERS:
        newValue = value
    else:
        newValue = -1

    return newValue


def convertUnits(value, currentUnit, newUnit):
    """
    Converts the given value from its current units to the desired units
    """
    newValue = 0

    switch = {
        Units.INCHES: toInches(value, currentUnit),
        Units.FEET: toFeet(value, currentUnit),
        Units.CENTIMETERS: toCentimeters(value, currentUnit),
        Units.METERS: toMeters(value, currentUnit),
    }

    newValue = switch.get(newUnit)
    return newValue

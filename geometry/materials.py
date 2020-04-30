class Materials:
    HARDWOOD = 0
    CARPET = 1
    DRYWALL = 2
    BRICK = 3
    CONCRETE = 4
    FOAM = 5

    @staticmethod
    def name(material: int):
        """
        Returns the string name of each material.
        """
        return {
            Materials.HARDWOOD: "Hardwood",
            Materials.CARPET: "Carpet",
            Materials.DRYWALL: "Drywall",
            Materials.BRICK: "Brick",
            Materials.CONCRETE: "Concrete",
            Materials.FOAM: "Foam",
        }.get(material, "")

    @staticmethod
    def absorption(material: int, freq: int) -> float:
        """
        Absorption coefficient at the given frequency
        """
        if material == Materials.HARDWOOD:
            return {
                125: 0.19,
                250: 0.23,
                500: 0.25,
                1000: 0.30,
                2000: 0.37,
                4000: 0.42,
            }.get(freq, 0)
        elif material == Materials.CARPET:
            return {
                125: 0.03,
                250: 0.09,
                500: 0.20,
                1000: 0.54,
                2000: 0.70,
                4000: 0.72,
            }.get(freq, 0)
        elif material == Materials.DRYWALL:
            return {
                125: 0.29,
                250: 0.10,
                500: 0.05,
                1000: 0.04,
                2000: 0.07,
                4000: 0.09,
            }.get(freq, 0)
        elif material == Materials.BRICK:
            return {
                125: 0.05,
                250: 0.04,
                500: 0.02,
                1000: 0.04,
                2000: 0.05,
                4000: 0.05,
            }.get(freq, 0)
        elif material == Materials.CONCRETE:
            return {
                125: 0.01,
                250: 0.01,
                500: 0.01,
                1000: 0.02,
                2000: 0.02,
                4000: 0.02,
            }.get(freq, 0)
        elif material == Materials.FOAM:
            return {
                125: 0.25,
                250: 0.50,
                500: 0.85,
                1000: 0.95,
                2000: 0.90,
                4000: 0.90,
            }.get(freq, 0)
        else:
            return 0

    @staticmethod
    def color(material: int):
        """
        Returns the color value of each material.
        """
        return {
            Materials.HARDWOOD: [0.34, 0.26, 0.01, 0.5],
            Materials.CARPET: [0.23, 0.40, 0.72, 0.5],
            Materials.DRYWALL: [0.92, 0.89, 0.78, 0.5],
            Materials.BRICK: [0.63, 0.09, 0, 0.5],
            Materials.CONCRETE: [0.45, 0.45, 0.45, 0.5],
            Materials.FOAM: [0.81, 0.77, 0.10, 0.5],
        }.get(material, [0, 0, 0, 0])

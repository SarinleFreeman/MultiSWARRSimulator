from src.Simulator.Generator.Definition.SWDelayLine.Antannae.definition import AntennaeI


class SWDelayLine:
    """
    The SWDelayLine class represents a Spin-Wave delay line. A spin wave delay line is a device that uses spin waves,
    which are collective excitations of the electron spins in a magnetic material, to store and transfer information.
     The spin waves can be excited and manipulated in various ways, such as by applying an external magnetic field or
      by injecting a microwave signal into the material. The class SWDelayLine represents a top-level model of a
       spin wave delay line, which includes properties such as the gyromagnetic ratio, saturation magnetization,
       and film thickness, as well as the antennae and damping coefficients used to excite and manipulate the spin waves.

    """

    def __init__(self, gyro_ratio: float, sat_mag: float, fm_thick:float, antannae: AntennaeI, nl_damp_coeff:float, l_damp_coeff:float):
        """
            Initializes the SWDelayLine class with the following parameters:
            :param gyro_ratio: The gyromagnetic ratio of the material of the delay line.
            :param sat_mag: The saturation magnetization of the material of the delay line.
            :param fm_thick: The thickness of the film material of the delay line.
            :param antannae:The antennae of the delay line.
            :param nl_damp_coeff: The non-linear damping coefficient of the delay line.
            :param l_damp_coeff: The linear damping coefficient of the delay line.
        """

        self.GYRO_RATIO = gyro_ratio
        self.SAT_MAG = sat_mag
        self.antannae = antannae
        self.FM_THICK = fm_thick
        self.nl_damp_coeff = nl_damp_coeff
        self.l_damp_coeff = l_damp_coeff

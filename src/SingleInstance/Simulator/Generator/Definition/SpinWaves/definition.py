from abc import ABC, abstractmethod
from typing import List

import numpy as np
from numpy import asarray, exp, sqrt, pi

from src.SingleInstance.Simulator.Generator.Definition.SWDelayLine.definition import SWDelayLine


class SpinWave(ABC):
    def __init__(self, sw_delay_line: SWDelayLine):
        """
        Initialize SpinWave class with a given SWDelayLine

        :param sw_delay_line: A delay line of given configuration.
        """
        self.sw_delay_line = sw_delay_line

    @abstractmethod
    def calculate_dispersion_relation_values(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:
        """
                This function calculates the dispersion relation values for a given set of k values and applied magnetic field.

                :param k_values: The k values for which the dispersion relation values need to be calculated
                :param app_mag: The applied magnetic field value
                :return: A list of dispersion relation values
                """
        pass

    @abstractmethod
    def calculate_non_linearity_coefficients(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:
        """
                Calculates the non-linearity coefficients for the given k_values and applied magnetic field.

                :param k_values: The k values for which to calculate the non-linearity coefficients
                :param app_mag: The applied magnetic field
                :return: The non-linearity coefficients for the given k_values
                """
        pass

    @abstractmethod
    def calculate_group_velocity(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:
        """
                Calculates the group velocities given k_values and applied magnetic field.

                :param k_values: The k values for which to calculate the non-linearity coefficients
                :param app_mag: The applied magnetic field
                :return: The group velocities
                """
        pass


class BVSW(SpinWave):
    """
    The following is a representation of a backward volume spin wave induced within a delay line of
    given configuration.
    """

    def __init__(self, sw_delay_line:SWDelayLine):
        super().__init__(sw_delay_line)

    def calculate_dispersion_relation_values(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:

        absolute_k_values = abs(asarray(k_values))

        def inner_val(k:float) -> float:
            """
            Helper function to calculate the inner value of the dispersion relation equation

            :param k: the current k value being considered
            :return: the inner value of the dispersion relation equation
            """
            if k == 0:
                f_k = 1
            else:
                f_k = (1 - exp(- k * self.sw_delay_line.FM_THICK)) / (
                        k * self.sw_delay_line.FM_THICK)

            return app_mag * (app_mag + self.sw_delay_line.SAT_MAG * f_k)

        total = asarray([inner_val(k) for k in absolute_k_values])
        return 2 * pi * self.sw_delay_line.GYRO_RATIO * sqrt(
            total
        ) / sqrt(2)

    def calculate_group_velocity(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:

        pass

    def calculate_non_linearity_coefficients(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:

        numerator = -0.5 * app_mag * self.sw_delay_line.SAT_MAG * self.sw_delay_line.GYRO_RATIO ** 2
        denominator = self.calculate_dispersion_relation_values(k_values=k_values, app_mag=app_mag)
        return numerator / denominator



class MSSW(SpinWave):
    """
    The following is a representation of a magnetostatic surface spin wave induced within a delay line of given configuration.
    """

    def __init__(self, sw_delay_line: SWDelayLine):
        super().__init__(sw_delay_line)

    def calculate_dispersion_relation_values(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:

        absolute_k_values = abs(asarray(k_values))


        a_0 = app_mag * (app_mag + self.sw_delay_line.SAT_MAG)

        # if k isn't 0
        a_1 = (self.sw_delay_line.SAT_MAG ** 2) / 4
        f_k = 1 - np.exp(-2 * absolute_k_values * self.sw_delay_line.FM_THICK)
        dispersion_values = self.sw_delay_line.GYRO_RATIO * sqrt(
            a_0 + a_1 * f_k
        )

        return 2 * pi * dispersion_values

    def calculate_group_velocity(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:
        """
        Calculate the group velocity for given k_values and applied magnetic field.

        :param k_values: The values of k for which to calculate the group velocity.
        :param app_mag: The applied magnetic field.
        :return: The calculated group velocity.
        """

        absolute_k_values = abs(asarray(k_values))
        a_1 = (self.sw_delay_line.SAT_MAG ** 2) / 4
        return (a_1 * self.sw_delay_line.FM_THICK * np.exp(-2 * absolute_k_values * self.sw_delay_line.FM_THICK) * (
                self.sw_delay_line.GYRO_RATIO ** 2)) / (
                   self.calculate_dispersion_relation_values(k_values, app_mag))

    def calculate_non_linearity_coefficients(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:
        numerator = -0.5 * app_mag * self.sw_delay_line.SAT_MAG * self.sw_delay_line.GYRO_RATIO ** 2

        denominator = self.calculate_dispersion_relation_values(k_values=k_values, app_mag=app_mag)
        return numerator / denominator


class FVSW(SpinWave):
    """
    The following is a representation of a forward volume spin wave induced within a delay line of
    given configuration.
    """

    def __init__(self, sw_delay_line: SWDelayLine):
        """
                Initialize FVSW class with a given SWDelayLine
                :param sw_delay_line: A delay line of given configuration.
                """
        super().__init__(sw_delay_line)

    def calculate_dispersion_relation_values(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:

        absolute_k_values = abs(asarray(k_values))

        def inner_val(k: float) -> float:
            """Inner function that calculates the
            inner value of the dispersion relation equation for a given k value.
                        """
            a_0 = app_mag - self.sw_delay_line.SAT_MAG
            if k == 0:
                a_1 = a_0
            else:
                f_k = (1 - exp(- k * self.sw_delay_line.FM_THICK)) / (
                        k * self.sw_delay_line.FM_THICK)
                a_1 = (app_mag - self.sw_delay_line.SAT_MAG * f_k)

            return a_0 * a_1

        total = asarray([inner_val(k) for k in absolute_k_values])
        return 2 * pi * self.sw_delay_line.GYRO_RATIO * sqrt(
            total
        ) / sqrt(2)

    def calculate_group_velocity(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:

        pass

    def calculate_non_linearity_coefficients(self, k_values: np.ndarray, app_mag: float) -> np.ndarray:

        numerator = self.sw_delay_line.SAT_MAG * (self.sw_delay_line.GYRO_RATIO ** 2) * (
                app_mag - self.sw_delay_line.SAT_MAG)

        denominator = self.calculate_dispersion_relation_values(k_values=k_values, app_mag=app_mag)
        return numerator / denominator

import abc
from numpy import abs, exp, asarray, argmax, array
from scipy.special import jv


class AntennaeI(metaclass=abc.ABCMeta):
    def __int__(self):
        self.filtered_signal = None

    def filter(self):
        pass


class BesselAntennae(AntennaeI):
    """
    The Bessel function is a special function that arises in many areas of physics and engineering, including solutions of
     differential equations and asymptotic expansions. In the context of this class, it is used in the filtering process of
     the spin wave spatial values.

    The Bessel function of the first kind, denoted by Jv(x), is defined as the solution of the Bessel differential equation:

    x^2*y'' + x*y' + (x^2 - v^2)*y = 0

    where v is a complex number.

    In the _sngle_enact_bessel_filter function, the Bessel function of the first kind is used in combination with exponential
    functions to calculate the filtered value of a given spatial spin wave value (k). The function returns 0 if the spatial
     spin wave value is less than or equal to zero or if the absolute value of k is greater than max_k/ant_width. Otherwise,
      it calculates the filtered value using the Bessel function and returns it.

    This filtered value is then used in the enact_bessel_filter function, where it is applied to all the spatial spin wave
     values in the self.sw_spatial_vals array, resulting in a new filtered signal. This filtered signal can then be further
     modified by the modulate_peak function to fit with experimental analysis, before being returned by the filter_signal
      function."""

    def __init__(self, ant_width: float, sw_spatial_vals: array, fm_thick: float, ant_in: int):
        """
        Initializes BesselAntennae class with the following parameters:
        :param ant_width: width of the antennae
        :param sw_spatial_vals: array of spatial spin wave values
        :param fm_thick: thickness of the film
        :param ant_in: input number of the antennae
        """

        self.sw_spatial_vals = sw_spatial_vals
        self.ant_width = ant_width
        self.fm_thick = fm_thick
        self.ant_in = ant_in
        self.filtered_signal = None


    def _sngle_enact_bessel_filter(self, k: float, shift_val: float, max_k: float) -> float:
        """
        :param k: spatial spin wave value to be filtered
        :param shift_val: shifting of filtering function peak
        :param max_k: max spatial spin wave value before reducing to 0 impact
        :return: filtered value
        """

        # Check if k is less than or equal to zero or if absolute_k is greater than max_k/ant_width
        absolute_k = abs(k)
        if k <= 0 or absolute_k > (max_k / self.ant_width):
            return 0
        else:
            # Calculate the filtered value using Bessel function and return it
            return exp(-1j * k * self.ant_in) * (
                    (jv(0, absolute_k * self.ant_width / 2) - jv(0, absolute_k * self.ant_width) * exp(
                        -absolute_k * shift_val)) * (1 - exp(-absolute_k * self.fm_thick)) / (
                            absolute_k * self.fm_thick))

    def enact_bessel_filter(self, shift_val=0.0005, max_k=4.8) -> None:
        """
        Applies Bessel filter to the spin wave spatial values
        :param shift_val: shifting of filtering function peak
        :param max_k: max spatial spin wave value before reducing to 0 impact
        """
        self.filtered_signal = asarray(
            [self._sngle_enact_bessel_filter(k, shift_val, max_k) for k in self.sw_spatial_vals])

    def modulate_peak(self, peak_width=2, gain=1.3):
        """
            Add extra gain to the peak to fit with experimental analysis.
            :param peak_width: The width of the peak to apply the gain to
            :param gain: The amount of extra gain to apply
            :return: None
            """

        # Find the index of the maximum value in the filtered signal
        max_val_index = argmax(self.filtered_signal)

        # Apply the gain to the section of the filtered signal surrounding the peak
        self.filtered_signal[max_val_index - peak_width:max_val_index + peak_width + 1] *= gain

    def filter(self) -> None:
        """
        Applies Bessel filter and modulates the peak of the filtered signal to fit with experimental analysis.
        """
        self.enact_bessel_filter()
        self.modulate_peak()

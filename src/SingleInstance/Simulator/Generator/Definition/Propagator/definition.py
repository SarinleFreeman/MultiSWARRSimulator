import copy
from typing import List

from numpy import conjugate, mean, multiply
from numpy.fft import fft, ifft

from src.SingleInstance.Simulator.Generator.Definition.Amplifier.definition import Amplifier


# define function capable of calculating landau-ginzburg non-linear term


class SpinWavePropagatorInterface:
    """
    The propagators job is to handle the propagation of spin waves over time. It uses various numerical differentiation
    techniques to achieve this.
    """

    def __init__(self, s_wave, wave_numbers: [int]):
        self.s_wave = s_wave
        self.wave_numbers = wave_numbers
        self.s_wave_g_velocities = None

    def propagate(self, s_wave_k_space_amps, time_step, absolving_function, amplifier, gain_modulation, current_time,
                  initial_time,output_antannae

                  ):
        pass

    def time_diff(self, *args):
        pass


class SimpleRungeKutta(SpinWavePropagatorInterface):
    """
    The Simple Runge Kutta class is a specific implementation of a spin-wave propagator. It utilizes the runge-kutta
    numerical differentiation technique to propagate the spin-wave. It has a simple non-linear term that is only
    calculated once to minimize the number of ffts.
    """

    def __init__(self, s_wave, wave_numbers: List[int], applied_magnetic_field):
        super().__init__(s_wave=s_wave, wave_numbers=wave_numbers)
        self.s_wave_ang_fs = s_wave.calculate_dispersion_relation_values(wave_numbers, applied_magnetic_field)
        self.s_wave_nl_cs = s_wave.calculate_non_linearity_coefficients(wave_numbers, applied_magnetic_field)
        self.s_wave_g_velocities = s_wave.calculate_group_velocity(wave_numbers, applied_magnetic_field)

    def l_ginz_non_linear_term(self, s_wave_input_amps, absolving_function):
        s_wave_x_space_amps = copy.deepcopy(s_wave_input_amps)
        non_linearity_comp = 1j * (self.s_wave_nl_cs - 1j * self.s_wave.sw_delay_line.nl_damp_coeff)
        squared_portion = multiply(conjugate(s_wave_x_space_amps), s_wave_x_space_amps)
        nl_part = multiply(squared_portion, s_wave_x_space_amps)

        abs_portion = multiply(s_wave_x_space_amps, absolving_function)
        non_linear_term = non_linearity_comp * nl_part - abs_portion

        return fft(non_linear_term)

    def time_diff(self, s_wave_k_space_amps,
                  nl_term, feedback_signal):
        """
        Parameters ----------
        s_wave_k_space_amps: Current spin wave amplitudes in k space.
        nl_terms: k-based fourier transform of i(N-iv)a|a|^2 where N is the non-linearity coefficient
        and v is the non-linear damping value defined by the nature of the spin wave and spin wave delay
        line respectively.
        Returns
        -------
        This return the value of the da(n,t)/dt at a specified time. It is used in the class to perform numerical
        propagation.
        """

        zeroth_angular_frequency = self.s_wave_ang_fs[50]

        ang_f_term = (self.s_wave_ang_fs - zeroth_angular_frequency)
        ang_comp = 1j * s_wave_k_space_amps * ang_f_term

        l_damp_comp = s_wave_k_space_amps * self.s_wave.sw_delay_line.l_damp_coeff

        return -ang_comp - nl_term - l_damp_comp + feedback_signal

    def propagate(self, s_wave_k_space_amps, time_step, absolving_function, amplifier:Amplifier, gain_modulation,
                  current_time, initial_time,output_antannae
                  ):
        """
        Parameters
        ----------
        s_wave_k_space_amps: spin wave amplitude in k space
        time_step: time step utilized in the runge kutta numerical differentiation technique
        amplifier: amplifier that amplifies noise
        absolving_function: This function is used to smoothly remove edge values.
        current_time: current spin wave time
        gain_modulation: modulation signal associated with gain
        Returns
        -------
        propagated_s_wave_k_space_amps
        The simple runge kuta process propagates the spin wave a wave by dt. It  calculates the computationally intense
        heavy non-linear calculation once , initially,  and assumes the rest are equivalent
        This is a spin_wave specific function, and it implicitly holds some information about the time_differential.
        """
        # copy waves
        copy_s_wave_k_space_amps = copy.deepcopy(s_wave_k_space_amps)
        s_wave_x_space = ifft(copy_s_wave_k_space_amps)

        nl_term = self.l_ginz_non_linear_term(s_wave_input_amps=s_wave_x_space,
                                              absolving_function=absolving_function)
        # Calculate feedback signal
        gain_signal =  amplifier.amplify(mean(s_wave_x_space[output_antannae:output_antannae+1])) * gain_modulation

        self.s_wave.sw_delay_line.antannae.filter()
        feed_back_signal = gain_signal * (
            self.s_wave.sw_delay_line.antannae.filtered_signal)

        # perform runge kutta
        k1_val = time_step * self.time_diff(copy_s_wave_k_space_amps,
                                            nl_term, feed_back_signal)

        k1_updated_amplitudes = copy_s_wave_k_space_amps + k1_val / 2

        k2_val = time_step * self.time_diff(k1_updated_amplitudes,
                                            nl_term, feed_back_signal)

        k2_updated_amplitudes = copy_s_wave_k_space_amps + k2_val / 2

        k3_val = time_step * self.time_diff(k2_updated_amplitudes,
                                            nl_term, feed_back_signal)
        k3_updated_amplitudes = copy_s_wave_k_space_amps + k3_val

        k4_val = time_step * self.time_diff(k3_updated_amplitudes,
                                            nl_term, feed_back_signal)

        # total propagation
        output = copy_s_wave_k_space_amps + (1 / 6) * (k1_val + 2 * k2_val + 2 * k3_val + k4_val)
        return output

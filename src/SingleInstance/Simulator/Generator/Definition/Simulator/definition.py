import copy
from typing import Tuple, Optional, List

import joblib
import numpy as np
import pandas as pd
import pickle

from numpy import random, zeros

from src.SingleInstance.Simulator.Generator.Definition.Amplifier.definition import Amplifier
from numpy.fft import fft, ifft

from src.SingleInstance.Simulator.Generator.Definition.Propagator.definition import SpinWavePropagatorInterface
from src.SingleInstance.Simulator.Generator.Definition.WaveGenerator.waveGenerator import BinaryWave
from src.Utils.load import loadall, load_latest
from src.Utils.prints import sprint, purprint


class Simulator:
    """
    The Simulator class is a simulation tool that uses a predefined propagation system, spin wave, and time step to simulate
     spin wave amplitudes. The class begins by initializing with a randomly complex state and uses a propagator to simulate the output.
      The class has several attributes, such as an Amplifier object, a propagator object, a time step, and a number of mesh points.
       The class also uses an absolving function to stop spin wave passing output antannae, and a gain value to counter loss
       and introduce more non-linear impacts. Additionally, the class has an option to input custom spin wave amplitudes
       and a binary wave. The class also has a simulate method which takes in several parameters such as number of steps,
        data directory, and verbose option, among others, and simulates the spin wave amplitudes using these attributes
        and parameters and saves the data in a  file.
    """

    def __init__(self, amplifier: Amplifier, propagator: SpinWavePropagatorInterface, time_step: float,
                 n_of_points: int, absolving_function: np.ndarray,
                 binary_wave: BinaryWave):
        # Amplifier object used in simulation
        self.amplifier = amplifier
        # Propagator object used in simulation
        self.propagator = propagator
        # Time step used in simulation
        self.time_step = time_step
        # Number of mesh points in simulation
        self.n_of_points = n_of_points
        # Absolving function used in simulation to stop spin wave passing output antannae
        self.absolving_function = absolving_function
        # binary wave
        self.binaryWave = binary_wave

    def simulate(self, number_of_steps: int, data_directory: str, verbose: bool = False, allocation_portion: int = 1,
                 shift_save: float = 0,
                 theta_int: float = 250e-9,
                 custom_start: str = None, const_bin=True, rounder=15) -> None:

        # check if values exist
        latest_k_values, latest_x_values, latest_time_value = get_latest_values(custom_start)

        # initialize s waves
        s_wave_amps_record_k, s_wave_amps_record_x = initialize_s_waves(
            number_of_steps=number_of_steps, allocation_portion=allocation_portion,
            n_of_points=self.n_of_points,
            latest_x_values=latest_x_values,
            latest_k_values=latest_k_values)

        # pre_calculate time  values
        current_time = latest_time_value
        previous_time = latest_time_value
        current_stored = np.copy(s_wave_amps_record_k[0])
        alloc_count = 0
        sprint('Beginning Propagation process')

        with open(
                data_directory,
                'ab') as f:
            for i in range(number_of_steps):
                if verbose:
                    purprint('-' * 100)
                    sprint('On Propagation Step {}/{}'.format(i, number_of_steps))

                # switch binary value if theta int has been passed
                if not const_bin:
                    rounded_time = round(current_time, rounder)
                    rounded_t_int = round(theta_int, rounder)
                    rounded_p_time = round(previous_time, rounder)
                    if round((rounded_time - rounded_p_time) / rounded_t_int, 3) == round(float(1),
                                                                                          3):
                        previous_time = copy.copy(current_time)
                        self.binaryWave.switch_bin_val()

                # Save data
                if current_time >= shift_save:
                    if i == 0 or i % allocation_portion == 0:
                        s_wave_amps_record_k[alloc_count] = np.copy(current_stored)
                        s_wave_amps_record_x[alloc_count] = ifft(np.copy(current_stored))
                        self.binaryWave.store_current()
                        alloc_count += 1
                        pickle.dump([
                            np.copy(current_stored), ifft(np.copy(current_stored)), current_time,
                            self.binaryWave.get_current()], f)

                # store the current amps before propagating
                previous_amps = np.copy(current_stored)
                current = self.propagator.propagate(previous_amps, time_step=self.time_step,
                                                    absolving_function=self.absolving_function,
                                                    amplifier=self.amplifier,
                                                    gain_modulation=self.binaryWave.get_current(),
                                                    current_time=current_time,
                                                    initial_time=latest_time_value, output_antannae=640)

                current_stored = np.copy(current)

                # store previous time and then update
                current_time = round(current_time + self.time_step, rounder)


def initialize_s_waves(number_of_steps: int, allocation_portion: int, n_of_points: int,
                       latest_x_values: Optional[np.ndarray] = None, latest_k_values: Optional[np.ndarray] = None) -> \
        Tuple[np.ndarray, np.ndarray]:
    """
        Initializes the s_wave_amps_record_k and s_wave_amps_record_x arrays, using the latest values if they exist.
        :param number_of_steps: Total number of steps in the simulation
        :param allocation_portion: The frequency at which the s wave values are stored
        :param n_of_points: The number of mesh points in the simulation
        :param latest_x_values: The latest x values of the s wave amplitudes
        :param latest_k_values: The latest k values of the s wave amplitudes
        :return: Tuple of s_wave_amps_record_k and s_wave_amps_record_x arrays
        """
    allocation_length = calculate_allocation_length(number_of_steps, allocation_portion)
    s_wave_amps_record_k = zeros([allocation_length, n_of_points], dtype=complex)
    s_wave_amps_record_x = zeros([allocation_length, n_of_points], dtype=complex)

    if latest_x_values is None and latest_k_values is None:
        rand_noisy_signal_in_x = create_noisy_signal(n_of_points=n_of_points)
        s_wave_amps_record_k[0] = fft(rand_noisy_signal_in_x)
        s_wave_amps_record_x[0] = rand_noisy_signal_in_x
    else:
        s_wave_amps_record_k[0] = latest_k_values
        s_wave_amps_record_x[0] = latest_x_values

    return s_wave_amps_record_k, s_wave_amps_record_x


def create_noisy_signal(n_of_points: int) -> np.ndarray:
    """
    Create a complex-valued noisy signal with length n_of_points
    :param n_of_points: length of the signal
    :return: complex-valued noisy signal
    """
    return ((random.random(n_of_points) - 0.5) + (
            random.random(n_of_points) - 0.5) * 1j) * 1e-12



def calculate_allocation_length(number_of_steps: int, allocation_portion: int) -> int:
    """
    Calculates the number of allocations needed to store the s wave amplitudes
    :param number_of_steps: Total number of steps in the simulation
    :param allocation_portion: The frequency at which the s wave values are stored
    :return: The number of allocations needed
    """
    if number_of_steps % allocation_portion == 0:
        return number_of_steps // allocation_portion
    else:
        return number_of_steps // allocation_portion + 1


def get_latest_values(custom_start: Optional[str]) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Retrieves the latest s wave amplitudes, x values, and time value from a file if they exist.
    :param custom_start: The file path where the data is stored
    :return: Tuple of latest s wave amplitudes in k-space, latest s wave amplitudes in x-space, and the latest time value
    """
    if custom_start is None:
        latest_k_values, latest_x_values, latest_time_value = None, None, 0
    else:
        print('here')
        print(custom_start)
        latest = load_latest(custom_start)
        print(latest)
        print(latest.shape)
        latest_k_values, latest_x_values, latest_time_value = latest[0], latest[1], latest[2]

        print(latest_k_values)
        print(latest_x_values)
        print(latest_time_value)
    return latest_k_values, latest_x_values, latest_time_value

def pre_calc_time(initial_time: float, time_step: float, number_of_steps: int, allocation_portion: int) -> List[float]:
    """
    Pre-calculates the times at which the s wave amplitudes are stored
    :param initial_time: The initial time at which the simulation starts
    :param time_step: The time step used in the simulation
    :param number_of_steps: Total number of steps in the simulation
    :param allocation_portion: The frequency at which the s wave values are stored
    :return: List of times at which the s wave amplitudes are stored
    """
    return [initial_time + step * time_step for step in range(number_of_steps) if step % allocation_portion == 0]


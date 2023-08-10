import numpy as np
from numpy import asarray, mean, absolute
from scipy.signal import savgol_filter

from src.Utils.load import loadall


class DataParser:
    def __init__(self, directory: str, output_antannae: int):
        self.output = None
        self.directory = directory
        self.output_antannae = output_antannae

    def load_data(self):
        self.output = asarray(loadall(self.directory), dtype=object)

    def get_k_amps(self):
        return asarray([element[0] for element in self.output])

    def get_x_amps(self):
        return asarray([element[1] for element in self.output])

    def get_output_x_amps(self):
        return asarray([
            mean(absolute(s_wave_and_time[1][
                          self.output_antannae - 1:self.output_antannae + 1])) for
            s_wave_and_time in
            self.output])

    def get_output_k_amps(self):
        return asarray([
            mean(absolute(s_wave_and_time[0][
                          self.output_antannae - 1:self.output_antannae + 1])) for
            s_wave_and_time in
            self.output])

    def get_bin_vals(self):
        return asarray([element[3] for element in self.output])

    def get_times(self):
        return asarray([element[2] for element in self.output])

    def get_transient_time(self, percentage=0.01):
        output_x_amps = self.get_output_x_amps()
        times = self.get_times()
        signal = output_x_amps

        # Take first derivative
        derivative = np.gradient(signal, times)

        # Smoothen the derivative to get the envelope
        window_size = 201  # This should be an odd number
        poly_order = 3  # Order of the polynomial used to fit the samples
        envelope = derivative
        num_smoothing_iterations = 100  # Number of times to apply the smoothing operation
        for _ in range(num_smoothing_iterations):
            envelope = savgol_filter(envelope, window_size, poly_order)

        # Ignore the part of the envelope before the peak
        peak_index = np.argmax(output_x_amps)
        envelope = envelope[peak_index:]
        times = times[peak_index:]

        # Iterate over the envelope to find the first time it enters the stationary regime
        stationary_time = times[-1]  # Default value in case the condition is never met
        stationary_index = -1
        for i in range(len(envelope)):
            if np.isclose(envelope[i], -1, atol=percentage):
                stationary_time = times[i]
                stationary_index = i
                break

        return stationary_time, stationary_index

    def get_index_at_x_percent(self, x=0.9):
        output_x_amps = self.get_output_x_amps()
        p_val = output_x_amps[-1] * x
        return np.where(output_x_amps >= p_val)[0][0]

    def get_k_amps_at_x_percent(self, x=0.9):
        index = self.get_index_at_x_percent(x)
        k_amps = np.absolute(self.get_k_amps())
        return k_amps[index]

    def get_phase_x(self):
        signal = np.asarray([
            np.mean(s_wave_and_time[1][self.output_antannae - 1:self.output_antannae + 1]) for
            s_wave_and_time in self.output])

        phase_x = np.unwrap(np.arctan2(signal.imag, signal.real))
        return phase_x


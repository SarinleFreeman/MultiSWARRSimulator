from numpy import asarray, mean, absolute
from src.Utils.load import loadall


class DataParser:
    def __init__(self, directory: str, output_antannae: int):
        self.output = None
        self.directory = directory
        self.output_antannae = output_antannae

    def load_data(self):
        self.output = asarray(loadall(self.directory))
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

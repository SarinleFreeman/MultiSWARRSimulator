import os

from matplotlib import pyplot as plt

from src.Utils.DataParser.definition import DataParser
from src.Utils.load import loadall


class SimVisualizer:
    """
    This class aims to save plots associated with a single simulation. You pass in a DataParser instance which links to
    a data directory. This is then reformatted and plotted for visualization purposes.
    """
    def __init__(self, fig_dir: str, data_parser: DataParser):
        self.fig_dir = fig_dir
        self.data_parser = data_parser

    def plot_output(self) -> None:

        # get time values
        times = self.data_parser.get_times()

        # get binary signal values
        binary = self.data_parser.get_bin_vals()

        # get output values
        output = self.data_parser.get_output_x_amps()

        fig, axs = plt.subplots(2)

        axs[0].plot(times, output, color='magenta')
        axs[0].set_title('Amplitude of signal at output')
        axs[0].set_xlabel('Seconds')
        axs[0].set_ylabel('Amplitude')

        ### corresponding binary signal

        axs[1].plot(times, binary)
        axs[1].set_title('Binary signal values')
        axs[1].set_xlabel('Seconds')
        axs[1].set_ylabel('Amplitude')

        fig.tight_layout()
        plt.savefig(self.fig_dir)
        plt.close()
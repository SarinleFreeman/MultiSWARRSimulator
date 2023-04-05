import os

from matplotlib import pyplot as plt
from numpy import ndarray

from src.Utils.DataParser.definition import DataParser
from src.Utils.load import loadall


class CapacityVisualizer:
    """
    This class aims to capacity calculation plots associated with a simulation. You pass in a STM and PC correalation
    values, and it gives you a visual output for the associated correalation values.
    """

    def __init__(self, cpc_fig_dir: str, cp_corr_vals: ndarray,  max_delay: int):
        # place to store pictures
        self.fig_dir = cpc_fig_dir

        # correalation values for all capacities and name
        self.cp_corr_vals = cp_corr_vals

        self.max_delay = max_delay

    def plot_corr_vals(self) -> None:
        # get x_range
        x_range = range(self.max_delay + 1)

        # plot capacities
        for name,corr_array in self.cp_corr_vals:
            plt.plot(x_range,corr_array,label=name)

        plt.title('Correlation values associated with STM and PC capacities')
        plt.ylabel('Correlation Value')
        plt.xlabel('Delays (theta_int)')
        plt.legend()
        plt.savefig(self.fig_dir)
        plt.close()

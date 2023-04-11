import os
from typing import List

from src.Paths.Constructors.PathConstructor import PathConstructor
from src.Utils.Handler.definition import AbstractHandler


class DynamicPathConstructor(PathConstructor):
    """
    This class is used to construct the path for the dynamic simulation. A dynamic simulation is a simulation that occurs
    after a base simulation. The base simulation is used to generate the initial conditions for the dynamic simulation.
    """

    def __init__(self, default_args: dict, number_of_signals: int, base_dir: str, inst_name: str
                 , handlers: List[AbstractHandler] = None):
        super().__init__(default_args, inst_name, handlers)
        self.number_of_signals = number_of_signals
        self.base_dir = base_dir

    def set_dirs(self):
        """
        Sets the directories for the simulation and the capacity calculations
        """
        # Directories for simulation
        self.args['sim_dir'] = self.base_dir
        self.args['custom_start'] = os.path.join(self.base_dir, "base_simulation_data")
        self.args['sim_vis_path'] = os.path.join(self.args['sim_dir'], f'dynamic_simulation_figure')
        self.args['sim_path'] = os.path.join(self.args['sim_dir'], f'dynamic_simulation_data')

        # Directories for Capacities
        self.args['stm_reconstructed_data_path'] = os.path.join(self.base_dir,
                                                                f'stm_reconstructed_data_path')
        self.args['stm_corr_data_path'] = os.path.join(self.base_dir, f'stm_corr_data_path')
        self.args['pc_reconstructed_data_path'] = os.path.join(self.base_dir,
                                                               f'pc_reconstructed_data_path')
        self.args['pc_corr_data_path'] = os.path.join(self.base_dir, f'pc_corr_data_path')

    def set_num_steps(self):
        """
        Sets the number of steps for the simulation
        """
        time_step = round(self.args['time_base'] ** (self.args['time_power']), self.args['fp_rounder'])
        run_time = self.number_of_signals * self.args['theta_int']
        self.args['number_of_steps'] = round(run_time / time_step)

    def set_const_bin(self):
        """
        Sets the constant binning to false
        """
        self.args['const_bin'] = False

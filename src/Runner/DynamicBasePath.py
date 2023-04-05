import os
from datetime import datetime

from src.Capacity.CapacityCalculations.PC.handler import PCCalcHandler
from src.Capacity.CapacityCalculations.STM.handler import STMCalcHandler
from src.Simulator.Generator.handler import SimGenHandler
from src.Simulator.Launcher.handler import SimLauncherHandler
from src.User.CLI.handler import CLIHandler
from src.Utils.Paths.definition import Path
from src.Visualizer.SimVisualizer.handler import SimVisHandler


class DynamicBasePath():
    def __init__(self, default_args: dict, number_of_signals: int, base_dir: str):
        self.args = default_args
        self.number_of_signals = number_of_signals
        self.base_dir = base_dir
        self.handlers = None

    def set_dirs(self, add_on=''):
        # simulation directories
        self.args['sim_dir'] = self.base_dir
        self.args['custom_start'] = os.path.join(self.base_dir, "base_simulation_data")
        self.args['sim_vis_path'] = os.path.join(self.args['sim_dir'], f'dynamic_simulation_figure {add_on}')
        self.args['sim_path'] = os.path.join(self.args['sim_dir'], f'dynamic_simulation_data {add_on}')

        # stm directories
        self.args['stm_reconstructed_data_path'] = os.path.join(self.base_dir,
                                                                f'stm_reconstructed_data_path {add_on}')
        self.args['stm_corr_data_path'] = os.path.join(self.base_dir, f'stm_corr_data_path {add_on}')
        self.args['pc_reconstructed_data_path'] = os.path.join(self.base_dir,
                                                               f'pc_reconstructed_data_path {add_on}')
        self.args['pc_corr_data_path'] = os.path.join(self.base_dir, f'pc_corr_data_path {add_on}')

    def set_num_steps(self):
        time_step = round(self.args['time_base'] ** (self.args['time_power']), self.args['fp_rounder'])
        run_time = self.number_of_signals * self.args['theta_int']
        self.args['number_of_steps'] = round(run_time / time_step)

    def set_const_bin(self):
        self.args['const_bin'] = False

    def set_handlers(self,handlers):
        self.handlers = handlers

    def build_path(self):
        # set dirs and handlers
        self.set_num_steps()
        self.set_const_bin()


        # generate path
        dynamic_path = Path(handlers=self.handlers)
        dynamic_path.generate_path()

        return dynamic_path

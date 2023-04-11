import os
from datetime import datetime
from typing import List

from src.Paths.Constructors.PathConstructor import PathConstructor
from src.Utils.Handler.definition import AbstractHandler


class BasePathConstructor(PathConstructor):
    def __init__(self, default_args: dict, inst_name: str, handlers: List[AbstractHandler] = None):
        super().__init__(default_args, inst_name, handlers)

    def set_dirs(self):
        self.args['sim_dir'] = os.path.join(os.getcwd(), 'simulation_data', f'{str(datetime.now())}{self.inst_name}')
        self.args['sim_vis_path'] = os.path.join(self.args['sim_dir'], 'base_simulation_figure')
        self.args['sim_path'] = os.path.join(self.args['sim_dir'], 'base_simulation_data')

    def set_num_steps(self):
        self.args['number_of_steps'] = round(5 * 1e10 * self.args['theta_int'])

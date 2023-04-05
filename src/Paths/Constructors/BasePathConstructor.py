import os
from datetime import datetime

from src.Paths.Constructors.PathConstructor import PathConstructor


class BasePathConstructor(PathConstructor):
    def __init__(self, default_args: dict,inst_name:str):
        super().__init__(default_args,inst_name)

    def set_dirs(self):
        self.args['sim_dir'] = os.path.join(os.getcwd(), 'simulation_data', f'{str(datetime.now())}{self.inst_name}')
        self.args['sim_vis_path'] = os.path.join(self.args['sim_dir'], 'base_simulation_figure')
        self.args['sim_path'] = os.path.join(self.args['sim_dir'], 'base_simulation_data')

    def set_handlers(self, handlers):
        self.handlers = handlers

    def set_num_steps(self, steps):
        self.args['number_of_steps'] = steps

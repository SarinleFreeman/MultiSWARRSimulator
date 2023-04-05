import os
from datetime import datetime

from src.SingleInstance.Simulator.DirCreator.handler import SimDirCreator
from src.SingleInstance.Simulator.Generator.handler import SimGenHandler
from src.SingleInstance.Simulator.Launcher.handler import SimLauncherHandler
from src.SingleInstance.User.CLI.handler import CLIHandler
from src.Paths.definition import Path
from src.SingleInstance.Visualizer.SimVisualizer.handler import SimVisHandler


class BasePathBuilder():
    def __init__(self, default_args: dict):
        self.args = default_args
        self.handlers = None

    def set_dirs(self, add_on=''):
        self.args['sim_dir'] = os.path.join(os.getcwd(), 'simulation_data', f'{str(datetime.now())}{add_on}')
        self.args['sim_vis_path'] = os.path.join(self.args['sim_dir'], 'base_simulation_figure')
        self.args['sim_path'] = os.path.join(self.args['sim_dir'], 'base_simulation_data')

    def set_handlers(self, handlers):
        self.handlers = handlers

    def set_num_steps(self,steps):
        self.args['number_of_steps'] = steps

    def build_path(self):
        # set dirs and handlers

        # generate path
        base_path = Path(handlers=self.handlers)
        base_path.generate_path()

        return base_path

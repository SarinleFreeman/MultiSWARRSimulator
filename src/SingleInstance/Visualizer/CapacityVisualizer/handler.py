from copy import copy

from src.Simulator.Generator.Builder.main import BuildSimulator
from src.Utils.DataParser.definition import DataParser
from src.Utils.Handler.definition import AbstractHandler
from src.Visualizer.SimVisualizer.definition import SimVisualizer


class CPCVisHandler(AbstractHandler):
    def __init__(self: 'CPCVisHandler', next_step='VisDirCreator'):
        self.next_step = next_step
        self.new_request = None
        self.name = 'CPC_VIS'

    def get_output(self):
        return self.new_request

    def handle(self: 'CPCVisHandler', request: dict) -> None:
        if request.get('TYPE') == "CPC_VIS":
            args = request.get('ARGS')

            #load parser
            data_parser = DataParser(args.get('sim_path'),args.get('output_antannae'))
            data_parser.load_data()

            sim_vis = SimVisualizer(fig_dir=args.get('sim_vis_path'), data_parser=data_parser)
            sim_vis.plot_output()

            # propagate request
            self.new_request = copy(request)
            self.new_request['TYPE'] = self.next_step
            super().handle(self.new_request)
        else:
            return super().handle(request)

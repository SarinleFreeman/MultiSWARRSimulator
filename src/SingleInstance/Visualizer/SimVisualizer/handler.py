from copy import copy

from src.SingleInstance.Simulator.Generator.Builder.main import BuildSimulator
from src.Utils.DataParser.definition import DataParser
from src.Utils.Handler.definition import AbstractHandler
from src.SingleInstance.Visualizer.SimVisualizer.definition import SimVisualizer


class SimVisHandler(AbstractHandler):
    def __init__(self: 'SimVisHandler', next_step='CPC_VIS'):
        self.next_step = next_step
        self.new_request = None
        self.name = 'SIM_VIS'

    def get_output(self):
        return self.new_request

    def handle(self: 'SimVisHandler', request: dict) -> None:
        if request.get('TYPE') == self.name:
            # build parser
            args = request.get('ARGS')
            # load data
            data_parser = DataParser(args.get('sim_path'), args.get('output_antannae'))
            data_parser.load_data()

            sim_vis = SimVisualizer(data_parser=data_parser, args=args)
            sim_vis.plot_x()
            sim_vis.plot_max_modes()
            sim_vis.plot_phase()
            sim_vis.plot_k_90()
            sim_vis.plot_binary()

            # propagate request
            self.new_request = copy(request)
            self.new_request['TYPE'] = self.next_step
            super().handle(self.new_request)
        else:
            return super().handle(request)

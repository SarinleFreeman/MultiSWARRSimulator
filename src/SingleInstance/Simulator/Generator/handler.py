from copy import copy

from src.SingleInstance.Simulator.Generator.Builder.main import BuildSimulator
from src.Utils.Handler.definition import AbstractHandler


class SimGenHandler(AbstractHandler):
    def __init__(self: 'SIM_LAUNCH', next_step=''):
        self.next_step = next_step
        self.new_request = None
        self.name = 'SIM_GEN'

    def get_output(self):
        return self.new_request

    def handle(self: 'SIM_GEN', request: dict) -> None:
        if request.get('TYPE') == self.name:

            # build simualtor
            build_simulator = BuildSimulator(args=request.get('ARGS'))
            simulator = build_simulator.build()



            # propagate request
            self.new_request = copy(request)
            self.new_request['TYPE'] = self.next_step
            self.new_request['ARGS']['sim'] = simulator
            super().handle(self.new_request)
        else:
            return super().handle(request)

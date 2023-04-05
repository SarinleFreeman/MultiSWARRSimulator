from copy import copy

from src.Utils.Handler.definition import AbstractHandler


class SimLauncherHandler(AbstractHandler):
    def __init__(self: 'SIM_LAUNCH', next_step=''):
        self.next_step = next_step
        self.new_request = None
        self.name = 'SIM_LAUNCH'

    def get_output(self):
        return self.new_request

    def handle(self: 'SIM_LAUNCH', request: dict) -> None:
        if request.get('TYPE') == self.name:
            # Launch Simulator
            simulator = request.get('ARGS').get('sim')



            simulator.simulate(number_of_steps=request.get('ARGS').get('number_of_steps'),
                                                          data_directory=request.get('ARGS').get('sim_path'),
                                                          verbose=request.get('ARGS').get('verbose'),
                                                          allocation_portion=request.get('ARGS').get('save_step'),
                                                          shift_save=request.get('ARGS').get('shift_save'),
                                                          theta_int=request.get('ARGS').get('theta_int'),
                                                          custom_start=request.get('ARGS').get('custom_start'),
                                                          const_bin=request.get('ARGS').get('const_bin'),
                                                          rounder = request.get('ARGS').get('fp_rounder')
                               )



            # propagate new request
            self.new_request = copy(request)
            self.new_request['TYPE'] = self.next_step
            super().handle(self.new_request)
        else:
            return super().handle(request)

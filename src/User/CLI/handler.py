import logging
from copy import copy

from numpy import pi
from numpy.fft import fftfreq

from src.User.CLI.definition import CLI
from src.Utils.Handler.definition import AbstractHandler


class CLIHandler(AbstractHandler):
    def __init__(self, next_step=''):
        self.next_step = next_step
        self.new_request = None
        self.name = 'CLI'


    def handle(self, request: dict) -> None:


        if request.get('TYPE') == self.name:
            # parse user inputs
            cli = CLI(defaults=request.get('ARGS'))
            cli.parse_user_inputs()
            new_args = cli.get_parsed_inputs()


            #generate wave numbers
            dz = new_args.get('antennae_seperation') / (
                    new_args.get('number_of_points') - 2 * new_args.get('strip_end_len'))

            wave_numbers = fftfreq(n=new_args.get('number_of_points'), d=dz) * 2 * pi
            new_args["dz"] = dz
            new_args['wave_numbers'] = wave_numbers



            # propagate request
            self.new_request = copy(request)
            self.new_request['TYPE'] = self.next_step
            self.new_request['ARGS'] = new_args

            super().handle(self.new_request)
        else:
            return super().handle(request)

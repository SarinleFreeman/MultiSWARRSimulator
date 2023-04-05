import os
from copy import copy

from src.Utils.DirCreator.dircreator import create_dir, store_args
from src.Utils.Handler.definition import AbstractHandler


class SimDirCreator(AbstractHandler):
    def __init__(self, next_step=''):
        self.new_request = None
        self.next_step = next_step
        self.name = 'SimDirCreator'

    def handle(self, request: dict) -> None:

        if request.get('TYPE') == self.name:
            # create dir and store args
            create_dir(path=request.get('ARGS').get('sim_dir'))
            store_args(path=os.path.join(request.get('ARGS').get('sim_dir'), 'args'), args=request.get('ARGS'))

            # propagate request
            self.new_request = copy(request)
            self.new_request['TYPE'] = self.next_step

            super().handle(self.new_request)
        else:
            return super().handle(request)

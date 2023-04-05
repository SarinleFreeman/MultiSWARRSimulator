from src.Utils.DirCreator.dircreator import create_dir
from src.Utils.Handler.definition import AbstractHandler


class CPCDirCreator(AbstractHandler):
    def __init__(self, next_step='STM_CALC'):
        self.next_step = next_step
        self.name = 'CPCDirCreator'

    def handle(self, request: dict) -> None:

        if request.get('TYPE') == "CPCDirCreator":
            # create dir
            create_dir(path=request.get('TYPE').get('ARGS').get('capacity_dir'))

            # propagate request
            propagate_new_request = {'TYPE': self.next_step, 'ARGS': request.get('ARGS')}
            super().handle(propagate_new_request)
        else:
            return super().handle(request)

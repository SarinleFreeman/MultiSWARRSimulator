from copy import copy

from src.SingleInstance.User.Validator.definition import Validator
from src.Utils.Handler.definition import AbstractHandler


class ValidatorHandler(AbstractHandler):
    def __init__(self: 'ValidatorHandler', next_step=''):
        self.next_step = next_step
        self.new_request = None
        self.name = 'VALIDATOR'

    def get_output(self):
        return self.new_request

    def handle(self: 'ValidatorHandler', request: dict) -> None:
        if request.get('TYPE') == "VALIDATE":
            # Create a Validator object with the params in the request
            validator = Validator(params=request.get('ARGS'))
            # Validate the params
            validator.validate()

            # propagate request
            self.new_request = copy(request)
            self.new_request['TYPE'] = self.next_step
            super().handle(self.new_request)
        else:
            # If the request type is not "VALIDATE", pass it to the next handler
            return super().handle(request)

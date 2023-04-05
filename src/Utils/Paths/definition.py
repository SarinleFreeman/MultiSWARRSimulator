import logging
from typing import List


from src.Utils.Handler.definition import AbstractHandler


class Path:
    """
    The path class connects handlers together to generate a path.
    """

    def __init__(self, handlers: List[AbstractHandler]):
        # Initialize list of handlers and the root handler
        self.handlers = handlers
        self.root_handler: AbstractHandler = handlers[0]

    def generate_path(self) -> None:

        # Connect handlers
        for i in range(len(self.handlers) - 1):
            self.handlers[i].set_next(self.handlers[i + 1])

        # set start point
        self.root_handler = self.handlers[0]

    def take_path(self, init_req: dict) -> None:
        try:
            # Try to handle the request
            self.root_handler.handle(init_req)
        except Exception as e:
            # Log any errors that occur while processing the request
            logging.info(f"An error occurred while processing the request: {e}")

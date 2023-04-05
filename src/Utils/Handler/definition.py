import logging
from abc import ABC, abstractmethod
from typing import Optional, Any, Callable

from simple_chalk import chalk


class Handler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    It also declares a method for executing a request.
    """

    @abstractmethod
    def set_next(self, handler: 'Handler') -> 'Handler':
        """
        Set the next handler in the chain.
        :param handler: the next handler
        :return: the next handler
        """
        pass

    @abstractmethod
    def handle(self, request: Any) -> Optional[str]:
        """
        Attempt to handle the request.
        :param request: the request to handle
        :return: the result of handling the request
        """
        pass


def handler_info(func: Callable) -> Callable:
    """
    Decorator function that uses logging to print information about the handler when the handle method is called.
    """

    def handler(self, request: Any) -> str:
        # Log a separator line

        # Log the name of the next handler in the chain
        if self._next_handler:
            logging.info(f'Now running {self._next_handler.name}')
        # Call the original handle method
        func(self, request)

    return handler


class AbstractHandler(Handler):
    _next_handler: Optional[Handler] = None

    def set_next(self, handler: Handler) -> Handler:
        """
        Set the next handler in the chain.
        :param handler: the next handler
        :return: the next handler
        """
        self._next_handler = handler
        return handler

    @abstractmethod
    @handler_info
    def handle(self, request: Any) -> None:
        """
        Attempt to handle the request by calling the handle method of the next handler in the chain.
        :param request: the request to handle
        """
        if self._next_handler:
            self._next_handler.handle(request)

        return None
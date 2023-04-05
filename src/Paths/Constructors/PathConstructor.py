import inspect
from abc import ABC, abstractmethod
from typing import List, Callable

from src.Paths.definition import Path
from src.Utils.Handler.definition import AbstractHandler


class PathConstructor(ABC):
    """
    The path constructor class is used to construct a path.
    """

    def __init__(self, default_args: dict, inst_name: str):
        """
        :param default_args: The default arguments for the path.
        :param inst_name: The name of the instance.
        """
        self.args = default_args
        self.inst_name = inst_name
        self.handlers = None

    @abstractmethod
    def set_dirs(self) -> None:
        """
        Set the directories for the path.
        """
        pass

    def set_handlers(self, handlers: List[AbstractHandler]) -> None:
        """
        Set the handlers for the path.
        """
        self.handlers = handlers

    def build_path(self) -> Path:
        """
        Build the path.
        """

        self.set_dirs()

        # Call all methods that start with "set_"
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith("set_") and name != "set_dirs" and name != "set_handlers":
                method()

        path = Path(handlers=self.handlers)
        path.generate_path()
        return path

import inspect
from abc import ABC, abstractmethod
from typing import List, Callable

from src.Paths.definition import Path
from src.Utils.Handler.definition import AbstractHandler


class PathConstructor(ABC):
    """
    The path constructor class is used to construct a path.
    """

    def __init__(self, default_args: dict, inst_name: str, handlers: List[AbstractHandler] = None):
        """
        :param default_args: The default arguments for the path.
        :param inst_name: The name of the instance.
        """
        self.args = default_args
        self.inst_name = inst_name
        self.handlers = handlers

    @abstractmethod
    def set_dirs(self) -> None:
        """
        Set the directories for the path.
        """
        pass

    def build_path(self, ignore_methods= []) -> Path:
        """
        Build the path.
        """

        # Call all the set methods and ignore certain methods.
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith("set_") and name not in ignore_methods:
                print(name)
                method()

        path = Path(handlers=self.handlers)
        path.generate_path()
        return path

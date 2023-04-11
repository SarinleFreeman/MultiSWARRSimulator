from typing import Any, List

from mpi4py import MPI
from numpy import asarray, array_split


class MPICommunicator:
    """
    This class is used to communicate between nodes.
    """

    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.size = self.comm.Get_size()
        self.rank = self.comm.Get_rank()

        self.root_splts = {}
        self.splt_pm = {}

    def share_params(self, name: str, rank=0):
        self.splt_pm[name] = self.comm.scatter(self.root_splts.get(name), root=rank)

    def split_params(self, name: str, space: List[Any]) -> None:
        try:
            self.root_splts[name] = array_split(asarray(space), self.size)
        except ValueError as e:
            print(f'Value Error: {e}')

    def share_variable(self, variable: Any, rank=0) -> Any:
        return self.comm.bcast(variable, root=rank)

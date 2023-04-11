from itertools import product as it_product
from copy import deepcopy
from typing import List, Any

import numpy as np
from numpy import linspace


class ParamGenerator:
    """
    This class generates a parameter space based on the provided default values and dimensions.
    """

    def __init__(self, defaults: dict):
        self.defaults = defaults
        self.dimensions = []
        self.space = []

    def add_dimensions(self, dimensions: List[List[Any]]) -> None:
        """
        This function adds multiple dimensions to our Parameter space.

        :param dimensions: List of dimensions to add.
        :return: None
        """
        for dim in dimensions:
            self.add_dimension(*dim)

    def add_dimension(self, name: str, min: float, max: float, num_of_points: int, rnd: int = 3) -> None:
        """
        This function adds a dimension to our Parameter space.

        :param name: Name of dimension.
        :param min: Minimum value of dimension.
        :param max: Maximum value of dimension.
        :param num_of_points: Number of points associated with dimension.
        :param rnd: Decimal place position we wish to round to.
        :return: None
        """
        # round limits and create array
        limits = np.round((min, max), rnd)
        nums = np.round(linspace(*limits, num_of_points), rnd)

        # create dimension and append to list
        dimension = list(it_product([name], nums))
        self.dimensions.append(dimension)

    def create_space(self) -> None:
        """
        This function creates the parameter space.

        :return: None
        """
        # create all combinations of dimensions
        dim_jnd = list(it_product(*self.dimensions))

        # create parameter space
        self.space = [
            {**deepcopy(self.defaults), **{var[0]: var[1] for var in elem},
             'identifier': ''.join(f'-{arg[0]}={arg[1]}' for arg in elem)}
            for elem in dim_jnd
        ]

        # Append theta int to the identifier
        for i, elem in enumerate(self.space):
            elem['identifier'] += f'-theta_int={self.defaults["theta_int"]}'
    def get_space(self) -> List[dict]:
        """
        This function returns the parameter space.

        :return: Parameter space.
        """
        return self.space

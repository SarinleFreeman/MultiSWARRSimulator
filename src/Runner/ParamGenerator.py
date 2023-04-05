import itertools
from copy import copy

import numpy as np
from numpy import arange, linspace


class ParamGenerator:
    def __init__(self,defaults:dict):
        self.defaults = defaults
        self.dimensions = []
        self.space = []

    def add_dimension(self, name: str, num_of_points: int, limits: tuple, rnd:int):
        """
        This function adds a dimension to our Parameter space.

        :param name: Name of dimension.
        :param num_of_points: Number of points associated with dimension.
        :param limits: Limits associated with dimension.
        :param rnd: Decimal place position we wish to round to.
        :return: None
        """
        limits = np.round(limits,rnd)

        nums = np.round(linspace(*limits,num_of_points), rnd)
        dimension = list(itertools.product([name], nums))
        self.dimensions.append(dimension)

    def create_space(self):
        #join dimensions
        dim_jnd = list(itertools.product(*self.dimensions))
        for elem in dim_jnd:
            df_copy = copy(self.defaults)
            df_copy.update({var[0]: var[1] for var in elem})

            #develop identification system
            identifier = ''
            for arg in elem:
                identifier += f'-{arg[0]}={arg[1]}'

            df_copy['identifier'] = identifier
            self.space.append(df_copy)
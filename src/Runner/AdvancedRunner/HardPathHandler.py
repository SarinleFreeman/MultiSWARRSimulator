from copy import copy

from src.Runner.AdvancedRunner.SoftPathHandler import SoftPathHandler


class HardPathHandler:
    """
    This class runs a set of Simulations. It takes in the following:

    1. The hard arguments are all associated with the immutable characteristics of a
    YIG fil.

    2. The soft arguments are associated with mutable characteristics such as gain or theta_int

    3. The default arguments are the unchanging default arguments associated with our simulation.


    The class uses this in-conjunction with the SoftPathHandler to run through all the combinations of hard - soft
    arguments to generate a set of output simulations.

    """

    def __init__(self, h_args: dict, s_args: dict, d_args: dict):
        """
        :param h_args: Varying hard arguments used in our base simulation and dynamic simulation.
        :param s_args: Varying soft arguments used in our dynamic simulation.
        :param d_args: Default arguments used in our dynamic simulation.

        """

        self.h_args = h_args
        self.s_args = s_args
        self.d_args = d_args

    def run_sims(self, bs_hlers: list, dy_hlers: list, init_req_type: str = 'CLI',num_signals: int = 50) -> None:
        """
        This function runs our combine Simulation.

        :param bs_hlers: Handlers associated with the base path.
        :param dy_hlers: Handlers associated with the base path.
        :param init_req_type: Initial request type for our base path.
        :param num_signals: Number of signals we generate in our dynamic paths.
        :return: None
        """

        for h_args in self.h_args:
            # Generate a copy of the hard-set args and combine them with the hard args.
            cmb_args = copy(self.d_args)
            cmb_args.update({var[0]: var[1] for var in h_args})

            # Construct new SoftPathHandler and construct the base path.
            sph = SoftPathHandler(args = cmb_args)
            sph.run_base_pth(bs_hlers=bs_hlers,init_req_type=init_req_type)

            # Run dynamic soft paths.
            sph.run_dynamic_pths(dy_hlers=dy_hlers,num_signals=num_signals)


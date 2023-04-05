from copy import copy

from src.Runner.BasePath import BasePathBuilder
from src.Runner.DynamicBasePath import DynamicBasePath


class SoftPathHandler:
    """
    This class runs a single Simulation path. It takes in a set of default arguments and a set of
     varying or soft arguments. This class generates the base path and can also generate the associated dynamic paths
     based on the varying/soft arguments.
    """

    def __init__(self, args: dict, s_args: dict):
        """
        :param args: Hard-set arguments used in our base simulation and dynamic simulation.
        :param s_args: Varying arguments used in our dynamic simulation.

        """
        self.args = args
        self.s_args = s_args

        # Arguments we used for generating our base simulation.
        self.base_args = None

    def run_base_pth(self, bs_hlers: list, init_req_type: str = 'CLI') -> None:
        """
        This function runs the base path for our simulation.
        :param bs_hlers: Handlers associated with the base path.
        :param init_req_type: Initial request type for our base path.
        :return: None
        """

        # Construct the base path.
        bs_p_b = BasePathBuilder(default_args=copy(self.args))
        bs_p_b.set_handlers(handlers=bs_hlers)
        bs_p_b.set_num_steps(round(5 * 1e12 * self.args['theta_int']))
        bs_pth = bs_p_b.build_path()

        # Take the path.
        bs_pth.take_path(init_req={'TYPE': init_req_type, 'ARGS': bs_p_b.args})

        # Store base args.
        self.base_args = bs_p_b.args

    def run_dynamic_pths(self,  dy_hlers: list, num_signals: int = 50, init_req_type: str = 'CLI') -> None:
        """
        This function runs the dynamic paths for our simulation.
        :param dy_hlers: Handlers associated with dynamic paths.
        :param init_req_type: Initial request type for our dynamic paths.
        :return: None
        """

        for s_arg in self.s_args:
            # Generate a copy of the hard-set args and update them with new soft args.
            arg_copy = copy(self.base_args)
            arg_copy.update({var[0]: var[1] for var in s_arg})


            # Generate dynamic path
            d_p_b = DynamicBasePath(default_args=arg_copy, number_of_signals=num_signals,
                                    base_dir=self.base_args.args['sim_dir'])
            d_p_b.set_handlers(handlers=dy_hlers)
            d_p_b.set_dirs(add_on=str(s_arg))
            d_pth = d_p_b.build_path()

            # Take dynamic path
            d_pth.take_path(init_req={'TYPE': init_req_type, 'ARGS': d_p_b.args})

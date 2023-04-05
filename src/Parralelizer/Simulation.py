import os
from copy import copy
import json
from src.Runner.BasePath import BasePathBuilder
from src.Runner.DynamicBasePath import DynamicBasePath
from src.Utils.prints import purprint, sprint


class SimPathRunner:
    """
    The goal of this class is to execute a set of Simulation paths and store the relevant data for further analysis.
    """

    def __init__(self, hp_space: list):
        """
        :param p_space: Parameter space.
        """
        self.hp_space = hp_space

    def run_sims(self, bs_hlers: list, dy_hlers: list, num_signals: int = 100, init_req_type: str = 'CLI') -> None:
        """
        The goal of this function is to run all of our simulations associated with our hyperparameter space.
        :param dy_hlers: Handlers associated with our dynamic path.
        :param num_signals: The number of theta_int signals generated in our dynamic path.
        :param init_req_type: Initial request type for our base and dynamic paths.
        :param bs_hlers: Handlers associated with the base path.
        :return: None
        """

        for count,args in enumerate(self.hp_space):
            #Inform user of count
            sprint(f"Running {args['identifier']}")
            sprint(f"{count+1}/{len(self.hp_space)}")

            # Build the base path.
            bs_p_b = BasePathBuilder(default_args=copy(args))
            bs_p_b.set_handlers(handlers=bs_hlers)
            bs_p_b.set_num_steps(round(5 * 1e10 * args['theta_int']))
            bs_p_b.set_dirs(add_on=args['identifier'])
            bs_p_b.args.pop('identifier')

            bs_pth = bs_p_b.build_path()

            # Take the base path.
            bs_pth.take_path(init_req={'TYPE': init_req_type, 'ARGS': bs_p_b.args})

            #Build the dynamic path.
            d_p_b = DynamicBasePath(default_args=copy(bs_p_b.args), number_of_signals=num_signals,
                                    base_dir=bs_p_b.args['sim_dir'])
            d_p_b.set_handlers(handlers=dy_hlers)
            d_p_b.set_dirs()
            d_pth = d_p_b.build_path()

            # Take dynamic path
            d_pth.take_path(init_req={'TYPE': init_req_type, 'ARGS': d_p_b.args})

            purprint('-' * 100)


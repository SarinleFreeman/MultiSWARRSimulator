import argparse

from mpi4py import MPI

from src.Parralelizer.ParamGenerator import ParamGenerator


class MPICommunicator:
    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.size = self.comm.Get_size()
        self.rank = self.comm.Get_rank()

    def setup_arguments(self,defaults):
        if self.rank == 0:
            parser = argparse.ArgumentParser(description="Simulation with custom theta_int")
            parser.add_argument("--theta_int", type=float, default=10e-9, help="Custom theta_int value")
            args = parser.parse_args()

            custom_theta_int = args.theta_int

            # Generate parameters for simulation
            pm_space = ParamGenerator(defaults=defaults)
            pm_space.add_dimension(name='gain', limits=(1, 3), num_of_points=16, rnd=1)
            pm_space.add_dimension(name='film_thickness', limits=(1e-6, 20e-6), num_of_points=32, rnd=7)
            pm_space.add_dimension(name='antennae_seperation', limits=(5e-3, 10e-3), num_of_points=5, rnd=4)
            pm_space.create_space()

            splitted_pm = split(asarray(pm_space.space), self.size)
        else:
            splitted_pm = None

        return self.comm.scatter(splitted_pm, root=0)
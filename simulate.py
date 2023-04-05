import os
import time
import psutil
import threading
from mpi4py import MPI
from numpy import split, asarray
import argparse 
from src.Capacity.CapacityCalculations.PC.handler import PCCalcHandler
from src.Capacity.CapacityCalculations.STM.handler import STMCalcHandler
from src.Runner.ParamGenerator import ParamGenerator
from src.Runner.Sim import SimPathRunner
from src.Simulator.DirCreator.handler import SimDirCreator
from src.Simulator.Generator.handler import SimGenHandler
from src.Simulator.Launcher.handler import SimLauncherHandler
from src.User.CLI.handler import CLIHandler
from src.Visualizer.SimVisualizer.handler import SimVisHandler


def monitor_memory_usage(interval = 1.0) -> None:
    """
    Monitor the memory usage of the current process and print the maximum memory usage.

    :param interval: Time interval (in seconds) between memory usage checks. Default is 1.0 seconds.
    """
    process = psutil.Process(os.getpid())
    max_memory = 0

    while True:
        current_memory = process.memory_info().rss  # Get the current memory usage in bytes
        max_memory = max(max_memory, current_memory)
        print(f"Current memory usage: {current_memory / 1024 / 1024:.2f} MB")
        print(f"Max memory usage: {max_memory / 1024 / 1024:.2f} MB")
        time.sleep(interval)
# set up communications
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
print(comm)
print(size)
print(rank)
monitor_thread = threading.Thread(target=monitor_memory_usage)
monitor_thread.daemon = True
monitor_thread.start()

# set up arguments
if rank == 0:
    parser = argparse.ArgumentParser(description="Simulation with custom theta_int")
    parser.add_argument("--theta_int", type=float, default=10e-9, help="Custom theta_int value")
    args = parser.parse_args()

    custom_theta_int = args.theta_int

    defaults = {'time_power': -9,
                'time_base': 10,
                'number_of_steps': 1,
                'number_of_points': 1024,
                'save_step': 1,
                'shift_save': 0,
                'theta_int': custom_theta_int,
                'max_delay': 10,
                'custom_start': None,
                'input_antannae': 384,
                'output_antannae': 640,
                'applied_mag_field': 1732,
                'gain_value': 1,
                'amp_noise_floor': 1e-3,
                'non_linear_damping_coefficient': 10 * 1e9,
                'linear_damping_coefficient': 4.4 * 1e6,
                'gyro_ratio': 2.8 * 1e6,
                'sat_mag_d_with_4_pi': 1919,
                'antennae_width': 50e-6,
                'film_thickness': 5.7e-6,
                'antennae_seperation': 8.2e-3,
                's_wave_type': 'MSSW',
                'short_term_memory': True,
                'parity_check': True,
                'plot': True,
                'strip_end_len': 384,
                'verbose': False,
                'const_bin': True,
                'fp_rounder': 15,
                'sim_dir': os.path.join(os.getcwd(), 'simulation_data', 'mssw_gain_fm_theta')

                }

    # Generate parameters for simulation
    pm_spce = ParamGenerator(defaults=defaults)
    pm_spce.add_dimension(name='gain', limits=(1, 3), num_of_points=16, rnd=1)
    pm_spce.add_dimension(name='film_thickness', limits=(1e-6, 20e-6), num_of_points=32, rnd=7)
    pm_spce.add_dimension(name='antennae_seperation', limits=(5e-3, 10e-3), num_of_points=5, rnd=4)
    pm_spce.create_space()

    splitted_pm = split(asarray(pm_spce.space), size)
else:
    splitted_pm = None

# Scatter parameters to each node.
splitted_set = comm.scatter(splitted_pm, root=0)

# Run calculations
sim = SimPathRunner(hp_space=splitted_set)
sim.run_sims(dy_hlers=[CLIHandler(next_step='SIM_GEN'),
                       SimGenHandler(next_step='SIM_LAUNCH'),
                       SimLauncherHandler(next_step='SIM_VIS')
                       ], bs_hlers=[CLIHandler(next_step='SimDirCreator'),
                                    SimDirCreator(next_step='SIM_GEN'),
                                    SimGenHandler(next_step='SIM_LAUNCH'),
                                    SimLauncherHandler(next_step='SIM_VIS')
                                    ], num_signals=500)

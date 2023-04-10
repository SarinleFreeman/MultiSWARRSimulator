import os
from numpy import linspace, round as np_round

from src.MultiCLI.MultiCli import MultiCLI
from src.Parralelizer.MPICommunicator import MPICommunicator
from src.Parralelizer.ParamGenerator import ParamGenerator
from src.Parralelizer.Simulation import SimPathRunner
from src.SingleInstance.Capacity.CapacityCalculations.STM.handler import STMCalcHandler
from src.SingleInstance.Simulator.DirCreator.handler import SimDirCreator
from src.SingleInstance.Simulator.Generator.handler import SimGenHandler
from src.SingleInstance.Simulator.Launcher.handler import SimLauncherHandler
from src.SingleInstance.User.CLI.handler import CLIHandler
from src.SingleInstance.Visualizer.SimVisualizer.handler import SimVisHandler


def run_simulations(splitted_set, dy_hlers: list = None, bs_hlers: list = None, num_signals: int = 500):
    # set up handlers
    if dy_hlers is None:
        dy_hlers = [CLIHandler(next_step='SIM_GEN'),
                    SimGenHandler(next_step='SIM_LAUNCH'),
                    SimLauncherHandler(next_step='SIM_VIS'),
                    SimVisHandler(next_step='STM_CALC'),
                    STMCalcHandler(next_step=None)
                    ]
    if bs_hlers is None:
        bs_hlers = [CLIHandler(next_step='SimDirCreator'),
                    SimDirCreator(next_step='SIM_GEN'),
                    SimGenHandler(next_step='SIM_LAUNCH'),
                    SimLauncherHandler(next_step='SIM_VIS'),
                    SimVisHandler(next_step=None)
                    ]
    # run simulations
    sim = SimPathRunner(hp_space=splitted_set)
    sim.run_sims(dy_hlers=dy_hlers, bs_hlers=bs_hlers, num_signals=num_signals)


# Setup Parallel Communications
mpi_comm = MPICommunicator()

# Get theta_int range from user and broadcast to all nodes
if mpi_comm.rank == 0:
    # Set up default parameters
    defaults = {'time_power': -9,
                'time_base': 10,
                'number_of_steps': 1,
                'number_of_points': 1024,
                'save_step': 1,
                'shift_save': 0,
                'theta_int': 10e-8,
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

    # Setup MultiCLI to acquire user inputs
    multi_cli = MultiCLI(defaults=defaults)
    multi_cli.parse_user_inputs()
    dim_inputs = multi_cli.get_parsed_inputs()

    # Remove theta_int from parsed inputs
    for count, p_input in enumerate(dim_inputs):
        if p_input[0] == 'theta_int':
            t_int_range = p_input
            dim_inputs.pop(count)
            break

    # Use default theta_int range if not specified
    try:
        t_int_range = np_round(linspace(t_int_range[1], t_int_range[2], t_int_range[3]), t_int_range[4])
    except NameError:
        t_int_range = np_round(linspace(defaults['theta_int'], defaults['theta_int'], 1), 7)
else:
    t_int_range = None

# Share theta_int range with all nodes and wait for synchronization
t_int_range = mpi_comm.share_variable(t_int_range)
mpi_comm.comm.Barrier()

# Run simulation for each theta_int
for t_int in t_int_range:
    # Generate Dimension Space to simulate
    if mpi_comm.rank == 0:
        # Generate Parameter Space for dynamic simulation variables
        defaults['theta_int'] = t_int
        pm_space = ParamGenerator(defaults=defaults)
        pm_space.add_dimensions(dim_inputs)
        pm_space.create_space()

        # Split parameter space into equal parts for each node
        mpi_comm.split_params(space=pm_space.get_space(), name='dynamic_params')

    # Share dynamic variables with all nodes and wait for synchronization
    mpi_comm.share_params(name='dynamic_params')
    mpi_comm.comm.Barrier()

    # Run all nodes
    print(
        f"Running on node {mpi_comm.rank}, with params: {[splt_set['identifier'] for splt_set in mpi_comm.splt_pm['dynamic_params']]}"
        )
    mpi_comm.comm.Barrier()

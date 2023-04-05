# define path
from datetime import datetime
import os

from src.Simulator.DirCreator.handler import SimDirCreator
from src.Simulator.Generator.handler import SimGenHandler
from src.Simulator.Launcher.handler import SimLauncherHandler
from src.User.CLI.handler import CLIHandler
from src.Utils.Paths.definition import Path
from src.Visualizer.SimVisualizer.handler import SimVisHandler



defaults = {
    "time_power": -9,
    "time_base": 10,
    "number_of_steps": 5500,
    "number_of_points": 1024,
    "save_step": 1,
    "shift_save": 0,
    "strip_end_len": 384,
    "theta_int": 1.1e-07,
    "max_delay": 10,
    "custom_start": None,
    "input_antannae": 384,
    "output_antannae": 640,
    "applied_mag_field": 1732,
    "gain_value": 1,
    "amp_noise_floor": 0.01,
    "non_linear_damping_coefficient": 10000000000.0,
    "linear_damping_coefficient": 4400000.0,
    "gyro_ratio": 2800000.0,
    "sat_mag_d_with_4_pi": 1919,
    "antennae_width": 5e-05,
    "film_thickness": 5.7e-06,
    "antennae_seperation": 0.0082,
    "s_wave_type": "MSSW",
    "short_term_memory": True,
    "parity_check": True,
    "plot": True,
    "sim_dir": "/home/moe/Documents/Physics-Research/final-code/SWARRNeuroSim/simulation_data/2023-03-08 17:44:13.073066-gain=1.0-theta_int=1.1e-07",
    "sim_vis_path": "/home/moe/Documents/Physics-Research/final-code/SWARRNeuroSim/simulation_data/2023-03-08 17:44:13.073066-gain=1.0-theta_int=1.1e-07/base_simulation_figure",
    "sim_path": "/home/moe/Documents/Physics-Research/final-code/SWARRNeuroSim/simulation_data/2023-03-08 17:44:13.073066-gain=1.0-theta_int=1.1e-07/base_simulation_data",
    "capacity_dir": None,
    "stm_reconstructed_data_path": None,
    "stm_corr_data_path": None,
    "pc_reconstructed_data_path": None,
    "pc_corr_data_path": None,
    "verbose": False,
    "const_bin": None,
    "fp_rounder": 15,
    "dz": 3.203125e-05,
    "wave_numbers": []
}

# store directory relevant information
current_date = str(datetime.now())
defaults['sim_dir'] = os.path.join(os.getcwd(), 'simulation_data', current_date)
defaults['sim_vis_path'] = os.path.join(defaults['sim_dir'], 'simulation_figure')
defaults['sim_path'] = os.path.join(defaults['sim_dir'], 'simulation_data')

defaults['stm_reconstructed_data_path'] = os.path.join(defaults['sim_dir'], 'stm_reconstructed_data_path')
defaults['stm_corr_data_path'] = os.path.join(defaults['sim_dir'], 'stm_corr_data_path')
defaults['pc_reconstructed_data_path'] = os.path.join(defaults['sim_dir'], 'pc_reconstructed_data_path')
defaults['pc_corr_data_path'] = os.path.join(defaults['sim_dir'], 'pc_corr_data_path')

# calculate wave numbers and associated information


handlers = [CLIHandler(next_step='SimDirCreator'),
            SimDirCreator(next_step='SIM_GEN'),
            SimGenHandler(next_step='SIM_LAUNCH'),
            SimLauncherHandler(next_step='SIM_VIS'),
            SimVisHandler(next_step=None)
            ]

main_path = Path(handlers=handlers)
main_path.generate_path()
main_path.take_path(init_req={'TYPE': 'CLI', 'ARGS': defaults})

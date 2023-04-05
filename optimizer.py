import os

print(os.getcwd())
from src.SingleInstance.User.CLI.handler import CLIHandler

from src.SingleInstance.Capacity.CapacityCalculations.PC.handler import PCCalcHandler
from src.SingleInstance.Capacity.CapacityCalculations.STM.handler import STMCalcHandler
from src.Paths.Constructors.DynamicPathConstructor import DynamicPathConstructor




# Define default variables
defaults = {
    "time_power": -9,
    "time_base": 10,
    "number_of_steps": 5500,
    "number_of_points": 1024,
    "save_step": 1,
    "shift_save": 0,
    "strip_end_len": 384,
    "theta_int": 20e-08,
    "max_delay": 10,
    "custom_start": None,
    "input_antannae": 384,
    "output_antannae": 640,
    "applied_mag_field": 1732,
    "gain_value": 2.1,
    "amp_noise_floor": 1e-05,
    "non_linear_damping_coefficient": 10000000000.0,
    "linear_damping_coefficient": 4400000.0,
    "gyro_ratio": 2800000.0,
    "sat_mag_d_with_4_pi": 1919,
    "antennae_width": 5e-05,
    "film_thickness": 1.081e-5,
    "antennae_seperation": 0.0082,
    "s_wave_type": "MSSW",
    "short_term_memory": True,
    "parity_check": True,
    "plot": True,
    "sim_dir":"/scratch/pawsey0841/myusuf/project/SWARRNeuroSim/14file/2023-03-20 14:03:29.387629-gain=2.1-film_thickness=1.081e-05",
    "sim_vis_path": "/home/moe/Documents/Physics-Research/final-code/SWARRNeuroSim/simulation_data/2023-03-10 10:19:15.118519-gain=1.0-theta_int=1.1e-07/base_simulation_figure",
    "sim_path": "/home/moe/Documents/Physics-Research/final-code/SWARRNeuroSim/simulation_data/2023-03-10 10:19:15.118519-gain=1.0-theta_int=1.1e-07/base_simulation_data",
    "capacity_dir": None,
    "stm_reconstructed_data_path": None,
    "stm_corr_data_path": None,
    "pc_reconstructed_data_path": None,
    "pc_corr_data_path": None,
    "verbose": True,
    "const_bin": True,
    "fp_rounder": 15,
    "dz": 3.203125e-05,
    "wave_numbers": []
}
"""#set up base path
bs_p_b = BasePathBuilder(default_args=defaults)
bs_p_b.build_path()
bs_pth = bs_p_b.build_path()
bs_pth.take_path(init_req={'TYPE': 'CLI', 'ARGS': bs_p_b.args})
"""

# set up dynamic path
d_p_b = DynamicPathConstructor(default_args=defaults, number_of_signals=500,
                               base_dir=os.path.join(os.getcwd(), '14file', '2023-03-20 14:03:29.387629-gain=2.1-film_thickness=1.081e-05'))
d_p_b.set_handlers(handlers=[
    CLIHandler(next_step='STM_CALC'),
    STMCalcHandler(next_step=None),
])
d_p_b.set_dirs()
d_pth = d_p_b.build_path()
# Take dynamic path
d_pth.take_path(init_req={'TYPE': 'STM_CALC', 'ARGS': d_p_b.args})


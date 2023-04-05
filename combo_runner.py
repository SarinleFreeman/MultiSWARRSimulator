import itertools

import numpy as np
from numpy import arange
from sklearn.utils.extmath import cartesian

from src.Runner.ParamGenerator import ParamGenerator

defaults = {'time_power': -9,
            'time_base': 10,
            'number_of_steps': 300,
            'number_of_points': 1024,
            'save_step': 1,
            'shift_save': 0,
            'theta_int': round(1e-7, 9),
            'max_delay': 10,
            'custom_start': None,
            'input_antannae': 384,
            'output_antannae': 640,
            'applied_mag_field': 1732,
            'gain_value': 2,
            'amp_noise_floor': 1e-8,
            'non_linear_damping_coefficient': 10 * 1e9,
            'linear_damping_coefficient': 4.4 * 1e6,
            'gyro_ratio': 2.8 * 1e6,
            'sat_mag_d_with_4_pi': 1919,
            'antennae_width': 50e-6,
            'film_thickness': 5.7e-6,
            'antennae_seperation': 8.2e-3,
            's_wave_type': "MSSW",
            'short_term_memory': True,
            'parity_check': True,
            'plot': True,
            'strip_end_len': 384,
            'verbose': True,
            'const_bin': True,
            'fp_rounder': 9

            }

pm_spce = ParamGenerator(defaults=defaults)

#add dimensions
pm_spce.add_dimension(name = 'film_thickness', limits=(10**-6,2*10**(-6)), rnding=6)
pm_spce.add_dimension(name = 'gain', limits=(1,2), rnding=1)
#add system
pm_spce.create_space()

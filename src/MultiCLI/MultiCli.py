import argparse
import os

import chalk
import numpy as np


class MultiCLI:
    def __init__(self: 'MultiCLI', defaults: dict) -> None:
        self.defaults = defaults
        self.args = None

    def parse_user_inputs(self: 'MultiCLI') -> None:
        parser = argparse.ArgumentParser(
            prog='main',
            description=print(chalk.blue.bold(
                'Welcome to the Multi-Dimensional Spin Wave Simulator. The program has a corresponding manual located '
                'at'
                'X explaining how to utilize the system effectively.'
                'I advise you to read said manual before use.\n '
            )),
        )

        # Add arguments for each parameter
        for key in self.defaults.keys():
            parser.add_argument(f'--{key}', f'-{key[:2]}', help=chalk.blue(
                f"This parameter is used to specify the range and the number of points for the {key} variable in the "
                "format min,max,num_points."),
                                type=str,
                                default=None)

        args = parser.parse_args()

        # Parse the arguments
        for key in self.defaults.keys():
            arg_value = getattr(args, key)
            if arg_value:
                arg_range = arg_value.split(',')
                if len(arg_range) == 3:
                    min_val = float(arg_range[0])
                    max_val = float(arg_range[1])
                    num_points = int(arg_range[2])

                    setattr(args, f'{key}_values', np.linspace(min_val, max_val, num_points).tolist())
                else:
                    raise ValueError(f"Invalid format for --{key}. It should be in the format min,max,num_points")

        self.args = args

    def get_parsed_inputs(self: 'MultiCLI') -> dict:
        return {
            k: getattr(self.args, k) if hasattr(self.args, k) else v
            for k, v in self.defaults.items()
        }

# test code
defaults = {'time_power': -9,
            'time_base': 10,
            'number_of_steps': 1,
            'number_of_points': 1024,
            'save_step': 1,
            'shift_save': 0,
            'theta_int': 10e-9
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

multi_cli = MultiCLI(defaults)
multi_cli.parse_user_inputs()
parsed_inputs = multi_cli.get_parsed_inputs()

print(parsed_inputs['theta_int_values'])
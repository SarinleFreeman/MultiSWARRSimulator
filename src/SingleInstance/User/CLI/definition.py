import argparse
from simple_chalk import chalk

from src.Utils.prints import success


class CLI:
    def __init__(self: 'CLI', defaults: dict) -> None:
        self.defaults = defaults
        self.args = None

    def parse_user_inputs(self: 'CLI') -> None:
        parser = argparse.ArgumentParser(
            prog='Single Instance',
            description=print(chalk.blue.bold(
                'Welcome to the Spin Wave Single Argument Simulator. The program has a corresponding manual located at '
                'X explaining how to utilize the system effectively.'
                'I advise you to read said manual before use.\n '
            )),
        )

        # Simulation Environment Variables (SEV)

        parser.add_argument('--time_power', '-tp',
                            help=chalk.blue(
                                "The time power parameter is used to specify the exponent value of the time step in "
                                "the simulation. The default value is taken from the provided defaults dictionary."),
                            type=int,
                            default=self.defaults.get('time_power'))
        parser.add_argument('--time_base', '-tb',
                            help=chalk.blue(
                                "The time base parameter is used to specify the base value of the time step in the "
                                "simulation. When combined with the time power parameter, it determines the actual "
                                "time step used in the simulation. The default value is taken from the provided "
                                "defaults dictionary."),
                            type=float,
                            default=self.defaults.get('time_base'))

        parser.add_argument('--number_of_steps', '-ns',
                            help=chalk.blue(
                                "This parameter specifies the number of steps that the simulation will run for. The "
                                "default value is taken from the provided defaults dictionary."),
                            type=int,
                            default=self.defaults.get('number_of_steps'))

        parser.add_argument('--number_of_points', '-n_p', help=chalk.blue(
            "This parameter specifies the number of mesh points that the simulation will run on. The default value is "
            "taken from the provided defaults dictionary."),
                            type=int,
                            default=self.defaults.get('number_of_points'))

        parser.add_argument('--save_step', '-s_s',
                            help=chalk.blue(
                                "This parameter specifies the number of steps to save the simulation data. The "
                                "default value is taken from the provided defaults dictionary."),
                            type=int,
                            default=self.defaults.get('save_step'))

        parser.add_argument('--shift_save', '-shft_sve',
                            help=chalk.blue(
                                "This parameter specifies the number of steps before the simulator starts saving data."),
                            type=int,
                            default=self.defaults.get('shift_save'))



        parser.add_argument('--strip_end_len', '-str_el',
                            help=chalk.blue(
                                "This parameter is used to specify the number of points associated with the end length of "
                                "the strip in the simulation. The default value is taken from the provided defaults "
                                "dictionary."),
                            type=int,
                            default=self.defaults.get('strip_end_len'))

        parser.add_argument('--theta_int', '-t_int', help=chalk.blue(
            "This parameter is used to specify the length of each part of the binary signal in the simulation. The "
            "default value is taken from the provided defaults dictionary."),
                            type=float,
                            default=self.defaults.get('theta_int'))

        parser.add_argument('--max_delay', '-m_dlay', help=chalk.blue(
            "This parameter is used to specify the maximum delay utilized within our capacity analysis, please see "
            "manual for more information."),
                            type=float,
                            default=self.defaults.get('max_delay'))
        parser.add_argument('--custom_start', '-c_start', help=chalk.blue(
            "This parameter is used to specify the custom starting point of the simulation, if desired. The default "
            "value is taken from the provided defaults dictionary."),
                            type=str,
                            default=self.defaults.get('custom_start'))

        parser.add_argument('--input_antannae', '-i_point', help=chalk.blue(
            "This parameter is used to specify the input, in points, the antannae is at"),
                            type=int,
                            default=self.defaults.get('input_antannae'))
        parser.add_argument('--output_antannae', '-o_point', help=chalk.blue(
            "This parameter is used to specify the input, in points, the antannae is at"),
                            type=int, default=self.defaults.get('output_antannae'))

        # Experimental Variables (SEV)

        parser.add_argument('--applied_mag_field', '-a_mag',
                            help=chalk.blue(
                                "This parameter specifies the strength of the external magnetic field applied in the simulation. The default value is taken from the provided defaults dictionary."),
                            type=float,
                            default=self.defaults.get('applied_mag_field'))

        parser.add_argument('--gain_value', '-g_val',
                            help=success(
                                "This parameter is used to calculate the base gain value for the simulation. The "
                                "default value is taken from the provided defaults dictionary."),
                            type=float,
                            default=self.defaults.get('gain_value'))

        parser.add_argument('--amp_noise_floor', '-a_nse',
                            help=chalk.blue(
                                "This parameter sets the base level of random noise that the amplifier produces."),
                            type=float,
                            default=self.defaults.get('amp_noise_floor'))

        parser.add_argument('--non_linear_damping_coefficient', '-n_dmp',
                            help=chalk.blue(
                                "This parameter sets the coefficient value for non-linear damping in the YIG film."),
                            type=float,
                            default=self.defaults.get('non_linear_damping_coefficient'))

        parser.add_argument('--linear_damping_coefficient', '-l_dmp',
                            help=chalk.blue("This parameter sets the coefficient value for linear damping in the YIG "
                                            "film."),
                            type=float,
                            default=self.defaults.get('linear_damping_coefficient'))

        parser.add_argument('--gyro_ratio', '-g_r',
                            help=chalk.blue("This parameter specifies the YIG films associated gyro-magnetic ratio."),
                            type=float,
                            default=self.defaults.get('gyro_ratio'))

        parser.add_argument('--sat_mag_d_with_4_pi', '-sat_mag',
                            help=chalk.blue("This parameter specifies the saturation magnetization constant , "
                                            "multiplied by 4*pi due to its nature in formulas."),
                            type=float,
                            default=self.defaults.get('sat_mag_d_with_4_pi'))

        parser.add_argument('--antennae_width', '-ant_w',
                            help=chalk.blue("This parameter specifies the width of our antennae."),
                            type=float,
                            default=self.defaults.get('antennae_width'))

        parser.add_argument('--film_thickness', '-fm_thick',
                            help=chalk.blue("This parameter specifies the thickness of our YIG film."),
                            type=float,
                            default=self.defaults.get('film_thickness'))

        parser.add_argument('--antennae_seperation', '-ant_sep',
                            help=chalk.blue(
                                "This parameter sets the seperation distance of the antennae in the simulation."),
                            type=float,
                            default=self.defaults.get('antennae_seperation'))

        parser.add_argument('--s_wave_type', '-swt',
                            help=chalk.blue(
                                "This parameter sets the type of spin wave that will be induced in the simulation."),
                            type=str,
                            default=self.defaults.get('s_wave_type'))
        # Capacity Task Variables (SEV)
        parser.add_argument('--short_term_memory', '-STM',
                            help=chalk.blue(
                                "This parameter specifies whether to calculate the short-term memory capacity."),
                            type=bool,
                            default=self.defaults.get('short_term_memory'))

        parser.add_argument('--parity_check', '-PC',
                            help=chalk.blue("This parameter specifies whether we wish to calculate the parity check "
                                            "memory capacity or not."),
                            type=bool,
                            default=self.defaults.get('parity_check'))

        # Storage Based Params (SB)

        parser.add_argument('--plot', '-plt',
                            help=chalk.blue(
                                "This parameter specifies whether we wish to plot our simulated data or not"),
                            type=bool,
                            default=self.defaults.get('plot'))

        parser.add_argument('--sim_dir', '-s_dir',
                            help=chalk.blue(
                                "This parameter specifies the directory where we store our simulation data."),
                            type=str,
                            default=self.defaults.get('sim_dir'))

        parser.add_argument('--sim_vis_path', '-sv_path',
                            help=chalk.blue(
                                "This parameter specifies the path we store our simulation image."),
                            type=str,
                            default=self.defaults.get('sim_vis_path'))

        parser.add_argument('--sim_path', '-s_path',
                            help=chalk.blue(
                                "This parameter specifies the path we store our simulation data."),
                            type=str,
                            default=self.defaults.get('sim_path'))

        parser.add_argument('--capacity_dir', '-cpc_dir',
                            help=chalk.blue(
                                "This parameter specifies where we store our associated capacity values."),
                            type=str,
                            default=self.defaults.get('capacity_dir'))



        parser.add_argument('--stm_reconstructed_data_path', '-stm_rc_pth',
                            help=chalk.blue(
                                "This parameter specifies where we store our reconstructed stm data."),
                            type=str,
                            default=self.defaults.get('stm_reconstructed_data_path'))

        parser.add_argument('--stm_corr_data_path', '-stm_cd_pth',
                            help=chalk.blue(
                                "This parameter specifies where we store our stm correlation data."),
                            type=str,
                            default=self.defaults.get('stm_corr_data_path'))

        parser.add_argument('--pc_reconstructed_data_path', '-pc_rc_pth',
                            help=chalk.blue(
                                "This parameter specifies where we store our reconstructed stm data."),
                            type=str,
                            default=self.defaults.get('pc_reconstructed_data_path'))

        parser.add_argument('--pc_corr_data_path', '-pc_cd_pth',
                            help=chalk.blue(
                                "This parameter specifies where we store our pc correlation data."),
                            type=str,
                            default=self.defaults.get('pc_corr_data_path'))

        # Misc
        parser.add_argument('--verbose', '-vb', help=chalk.blue(
            "This parameter is used to specify whether we want to have print statements or not"),
                            type=bool,
                            default=self.defaults.get('verbose'))

        parser.add_argument('--const_bin', '-cb',
                            help=chalk.blue(
                                "This parameter specifies whether we want to keep a constant binary or oscillating one"
                                ),
                            type=bool,
                            default=self.defaults.get('const_bin'))

        parser.add_argument('--fp_rounder', '-f_r',
                            help=chalk.blue(
                                "This parameter specifies what level do you want our times to be rounded at"
                            ),
                            type=bool,
                            default=self.defaults.get('fp_rounder'))

        args = parser.parse_args()

        self.args = args

    def get_parsed_inputs(self: 'CLI') -> dict:
        return namespace_to_dict(self.args)


def namespace_to_dict(namespace: argparse.Namespace) -> dict:
    return {
        k: namespace_to_dict(v) if isinstance(v, argparse.Namespace) else v
        for k, v in vars(namespace).items()
    }

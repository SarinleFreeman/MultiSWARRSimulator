import ipaddress


class Validator:
    def __init__(self: 'Validator', params: dict) -> None:
        self.params = params
        # validation
        self.validations = [(self.params.get('save_step'), val_save_step),
                            (self.params.get('s_wave_type'), val_s_wave_type),
                            (self.params.get('number_of_steps'), val_number_of_steps),
                            (self.params.get('applied_mag_field'), val_applied_mag_field),
                            (self.params.get('amp_noise_floor'), val_amp_noise_floor),
                            (self.params.get('gyro_ratio'), val_gyro_ratio),
                            (self.params.get('saturation_magnetization'), val_saturation_magnetization),
                            (self.params.get('antennae_width'), val_antennae_width),
                            (self.params.get('film_thickness'), val_film_thickness),
                            (self.params.get('antennae_seperation'), val_antennae_seperation),
                            (self.params.get('number_of_points'), val_number_of_points),
                            (self.params.get('time_base'), val_time_base),
                            (self.params.get('short_term_memory'), val_short_term_memory)
                             ]

    def validate(self):
        # run validations
        for val_pair in self.validations:
            val_pair[1](val_pair[0])


def val_save_step(save_step: int) -> None:
    if save_step < 1:
        raise Exception('The save step must be bigger than one!')


def val_s_wave_type(s_wave_type: str, possible_types=['MSSW', 'BVSW', 'FVSW']) -> None:
    if s_wave_type.upper() not in possible_types:
        raise Exception('The spin wave type does not exist!')


def val_number_of_steps(number_of_steps: int) -> None:
    if number_of_steps <= 0:
        raise Exception('The number of steps must be greater than zero!')




def val_applied_mag_field(applied_mag_field: float) -> None:
    if applied_mag_field < 0:
        raise Exception('The applied magnetic field must be greater than or equal to zero!')


def val_gyro_ratio(gyro_ratio: float) -> None:
    if gyro_ratio <= 0:
        raise Exception('The gyromagnetic ratio value must be greater than zero!')


def val_saturation_magnetization(saturation_magnetization: float) -> None:
    if saturation_magnetization <= 0:
        raise Exception('The saturation magnetization value must be greater than zero!')


def val_antennae_width(antennae_width: float) -> None:
    if antennae_width <= 0:
        raise Exception('The antennae width value must be greater than zero!')


def val_film_thickness(film_thickness: float) -> None:
    if film_thickness <= 0:
        raise Exception('The film thickness value must be greater than zero!')


def val_antennae_seperation(antennae_seperation: float) -> None:
    if antennae_seperation <= 0:
        raise Exception('The antennae separation value must be greater than zero!')


def val_number_of_points(number_of_points: int) -> None:
    if number_of_points <= 0:
        raise Exception('The number of points must be greater than zero!')


def val_time_base(time_base: float) -> None:
    if time_base <= 0:
        raise Exception('The time base value must be greater than zero!')


def val_amp_noise_floor(amp_noise_floor: float) -> None:
    if amp_noise_floor <= 0:
        raise Exception('The amplitude noise floor value must be greater than zero!')


def val_short_term_memory(short_term_memory: bool) -> None:
    if not isinstance(short_term_memory, bool):
        raise Exception('The short term memory value must be a boolean!')


def val_parity_check(parity_check: bool) -> None:
    if not isinstance(parity_check, bool):
        raise Exception('The parity check value must be a boolean!')

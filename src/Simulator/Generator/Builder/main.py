from array import array

from numpy import pi, linspace, arctan, array, zeros, concatenate, ndarray

from src.Simulator.Generator.Definition.Amplifier.definition import Amplifier
from src.Simulator.Generator.Definition.Propagator.definition import SimpleRungeKutta, SpinWavePropagatorInterface
from src.Simulator.Generator.Definition.SWDelayLine.Antannae.definition import AntennaeI, BesselAntennae
from src.Simulator.Generator.Definition.SWDelayLine.definition import SWDelayLine
from src.Simulator.Generator.Definition.Simulator.definition import Simulator
from src.Simulator.Generator.Definition.SpinWaves.definition import MSSW, BVSW, FVSW, SpinWave
from src.Simulator.Generator.Definition.WaveGenerator.waveGenerator import BinaryWave

"The BuildSimulator class is used to construct the various components of the Simulator class, such as the amplifier," \
" antannae, spin wave delay line, spin wave, and propagator. The class takes in an argument of a dictionary containing the necessary parameters for each component's initialization. For example, the build_amplifier method initializes an Amplifier object with the gain value and noise floor specified in the argument dictionary. "


class BuildSimulator:
    def __init__(self, args):
        self.args = args

    def build_amplifier(self) -> Amplifier:
        return Amplifier(gain=2700 * self.args.get('linear_damping_coefficient'),
                         noise_floor=self.args.get('amp_noise_floor'))

    def build_antannae(self) -> AntennaeI:

        return BesselAntennae(ant_width=self.args.get('antennae_width'), sw_spatial_vals=self.args.get('wave_numbers'),
                              fm_thick=self.args.get('film_thickness'),
                              ant_in=self.args.get('input_antannae') * self.args.get('dz'))

    def build_sw_delayline(self, antannae: AntennaeI) -> SWDelayLine:
        return SWDelayLine(gyro_ratio=self.args.get('gyro_ratio'), sat_mag=self.args.get('sat_mag_d_with_4_pi'),
                           fm_thick=self.args.get('film_thickness'), antannae=antannae,
                           nl_damp_coeff=self.args.get('non_linear_damping_coefficient'),
                           l_damp_coeff=self.args.get('linear_damping_coefficient'))

    def build_s_wave(self, sw_delay: SWDelayLine) -> SpinWave:
        s_wave_type = self.args.get('s_wave_type')
        # return spin wave depending on type given
        if s_wave_type == 'MSSW':
            s_wave = MSSW(sw_delay_line=sw_delay)
        elif s_wave_type == 'BVSW':
            s_wave = BVSW(sw_delay_line=sw_delay)
        elif s_wave_type == 'FVSW':
            s_wave = FVSW(sw_delay_line=sw_delay)
        else:
            raise Exception('SPIN WAVE TYPE DOES NOT EXIST')

        return s_wave

    def build_propagator(self, swave: SpinWave) -> SpinWavePropagatorInterface:
        # calculate the spatial resolution
        # calculate the associated wave numbers to use in propagation.

        return SimpleRungeKutta(s_wave=swave, wave_numbers=self.args.get('wave_numbers'),
                                applied_magnetic_field=self.args.get('applied_mag_field'))

    def build_absolving_loss(self) -> ndarray:

        lst = array([arctan(xxx) for xxx in linspace(-9, 9, self.args.get('strip_end_len') - 20)])
        blocker = ((lst + arctan(9)) / pi) * -50 * 1e-2
        return concatenate((blocker[::-1],
                            zeros(self.args.get('number_of_points') - 2 * (self.args.get('strip_end_len') - 20)),
                            blocker))

    def build_binary_wave(self) -> BinaryWave:
        return BinaryWave(init_val=self.args.get('gain_value'),
                          mapping=(round(self.args.get('gain_value'), 1), round(self.args.get('gain_value') * 1.1, 1)))

    def build(self) -> Simulator:
        amplifier = self.build_amplifier()

        antannae = self.build_antannae()
        sw_delay_line = self.build_sw_delayline(antannae=antannae)

        s_wave = self.build_s_wave(sw_delay=sw_delay_line)

        propagator = self.build_propagator(swave=s_wave)

        time_step = (self.args.get('time_base')) ** self.args.get('time_power')
        absolving_func = self.build_absolving_loss()
        binary_wave = self.build_binary_wave()

        return Simulator(amplifier=amplifier, propagator=propagator, time_step=time_step,
                         n_of_points=self.args.get('number_of_points')
                         , absolving_function=absolving_func,
                         binary_wave=binary_wave)

from numpy import ndarray

from src.Capacity.CapacityCalculations.Definition.CapacityCalculator.definition import CapacityCalculator
from src.Utils.DataParser.definition import DataParser
from src.Capacity.CapacityCalculations.Definition.Sampler.definition import SignalSampler
from src.Capacity.CapacityCalculations.PC.definition import PCCapacityCalculator
from src.Capacity.CapacityCalculations.STM.definition import STMCapacityCalculator


class CapacityCalculatorBuilder:
    def __init__(self, args, calc_type):
        self.args = args
        self.calc_type = calc_type

    def build_data_paraser(self) -> DataParser:
        return DataParser(self.args.get('sim_path'), self.args.get('output_antannae'))

    def build_calculator(self, time_values: ndarray, output_amps: ndarray, bins: ndarray,
                         sampler: SignalSampler) -> CapacityCalculator:
        print(self.calc_type)

        if self.calc_type == 'STM':
            return STMCapacityCalculator(time_values=time_values, theta_int=self.args.get('theta_int'),
                                         output_amps=output_amps,
                                         bin_values=bins,
                                         sampler=sampler)
        elif self.calc_type == 'PC':
            return PCCapacityCalculator(time_values=time_values, theta_int=self.args.get('theta_int'),
                                        output_amps=output_amps,
                                        bin_values=bins,
                                        sampler=sampler)
        else:
            raise ValueError('Incorrect calculator type, please specify type of capacity calculator.')

    def build_sampler(self) -> SignalSampler:
        return SignalSampler()

    def build(self):
        dparser = self.build_data_paraser()
        dparser.load_data()
        calc = self.build_calculator(time_values=dparser.get_times(), output_amps=dparser.get_output_x_amps(),
                                     bins=dparser.get_bin_vals(),
                                     sampler=self.build_sampler())
        return calc


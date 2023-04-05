import json
from copy import copy

from src.Capacity.CapacityCalculations.Definition.CapacityCalculator.builder import CapacityCalculatorBuilder
from src.Capacity.CapacityCalculations.Definition.CapacityCalculator.definition import calculate_corr_coefs
from src.Capacity.CapacityCalculations.PC.definition import gen_y_pc
from src.Utils.Handler.definition import AbstractHandler


class PCCalcHandler(AbstractHandler):
    def __init__(self: 'PCCalcHandler', next_step):
        self.next_step = next_step
        self.new_request = None
        self.name = 'PC_CALC'

    def get_output(self):
        return self.new_request

    def handle(self: 'PCCalcHandler', request: dict) -> None:
        if request.get('TYPE') == self.name:
            # build calculator
            builder = CapacityCalculatorBuilder(request.get('ARGS'), 'PC')
            pc_calc = builder.build()

            # split half the data into training and the other half into testing.
            splt_amps, av_splt_bins = pc_calc.split_data(rounder=request.get('ARGS').get('fp_rounder'))

            half = len(splt_amps) // 2
            x_test = splt_amps[:half]
            y_test = av_splt_bins[:half]

            x_train = splt_amps[half: 2 * half]
            y_train = av_splt_bins[half: 2 * half]

            # fit training data to calculator
            pc_calc.fit_data(x_train, y_train)

            # check if we can transform data
            if request.get('ARGS').get('max_delay') >= half:
                raise Exception(
                    f'Not enough data to perform STM capacity analysis on, please reduce max_delay to {half - 1}')

            # transform data and generate regressors
            pc_calc.transform_data(max_delay=request.get('ARGS').get('max_delay'))
            pc_calc.generate_regressors()

            #predict and store data
            prediction = pc_calc.predict(x=x_test[request.get('ARGS').get('max_delay'):])
            actual = gen_y_pc(max_delay=request.get('ARGS').get('max_delay'), y=y_test)





            # store stm and propagate new request
            self.new_request = copy(request)
            self.new_request['TYPE'] = self.next_step
            self.new_request['ARGS']['pc_corr_values'] = calculate_corr_coefs(y_pred=prediction,
                                                                               y=actual)
            self.new_request['ARGS']['pc_graphs'] = {'pc_actual': actual.tolist(), 'pc_predicted': prediction.tolist()}

            #store data
            # save correalation values
            with open(request.get('ARGS').get('pc_corr_data_path'), "w") as outfile:
                pc_corr_json = json.dumps(self.new_request['ARGS']['pc_corr_values'], indent=4)
                outfile.write(pc_corr_json)

            with open(request.get('ARGS').get('pc_reconstructed_data_path'), "w") as outfile:
                pc_rcnst_json = json.dumps(self.new_request['ARGS']['pc_graphs'], indent=4)
                outfile.write(pc_rcnst_json)




        else:
            return super().handle(request)

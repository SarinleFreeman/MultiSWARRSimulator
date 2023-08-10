import json
from copy import copy

import numpy as np
from matplotlib import pyplot as plt
from numpy import corrcoef

from src.SingleInstance.Capacity.CapacityCalculations.Definition.CapacityCalculator.builder import \
    CapacityCalculatorBuilder
from src.SingleInstance.Capacity.CapacityCalculations.Definition.CapacityCalculator.definition import \
    calculate_corr_coefs
from src.SingleInstance.Capacity.CapacityCalculations.STM.definition import gen_y_stm
from src.Utils.Handler.definition import AbstractHandler


class STMCalcHandler(AbstractHandler):
    def __init__(self: 'STMCalcHandler', next_step='PC_CALC'):
        self.next_step = next_step
        self.new_request = None
        self.name = 'STM_CALC'

    def get_output(self):
        return self.new_request

    def handle(self: 'STMCalcHandler', request: dict) -> None:
        if request.get('TYPE') == self.name:
            # build calculator

            builder = CapacityCalculatorBuilder(request.get('ARGS'), 'STM')

            stm_calc = builder.build()

            # split half the data into training and the other half into testing.

            splt_amps, av_splt_bins = stm_calc.split_data(rounder=request.get('ARGS').get('fp_rounder'))

            # DECOUPLING
            buffer = int(0.1*len(av_splt_bins))  # define the size of the buffer

            total_len = len(splt_amps)
            half = (total_len - buffer) // 2

            x_train = splt_amps[:half]
            y_train = av_splt_bins[:half]

            x_test = splt_amps[half + buffer: 2 * half + buffer]
            y_test = av_splt_bins[half + buffer: 2 * half + buffer]


            # fit training data to calculator
            stm_calc.fit_data(x_train, y_train)


            # check if we can transform data
            if request.get('ARGS').get('max_delay') >= half:
                raise Exception(
                    f'Not enough data to perform STM capacity analysis on, please reduce max_delay to {half - 1}')

            # transform data and generate regressors
            stm_calc.transform_data(max_delay=request.get('ARGS').get('max_delay'))

            stm_calc.generate_regressors()

            # predict and store data
            prediction = stm_calc.predict(x=x_test[request.get('ARGS').get('max_delay'):])

            actual = gen_y_stm(max_delay=request.get('ARGS').get('max_delay'), y=y_test)
            #np.save(f'/home/moe/Documents/Physics-Research/Multi_Swarr_Data_Analysis/stm_dir/{request.get("ARGS").get("identifier")}_prediction.npy', prediction)
            #np.save(f'/home/moe/Documents/Physics-Research/Multi_Swarr_Data_Analysis/stm_dir/{request.get("ARGS").get("identifier")}_actual.npy', actual)
            #exit()
            # store stm and propagate new request
            self.new_request = copy(request)
            self.new_request['TYPE'] = self.next_step
            self.new_request['ARGS']['stm_corr_values'] = calculate_corr_coefs(y_pred=prediction, y=actual)
            self.new_request['ARGS']['stm_graphs'] = {'stm_actual': actual.tolist(),
                                                      'stm_predicted': prediction.tolist()}

            # save correalation values
            with open(request.get('ARGS').get('stm_corr_data_path'), "w") as outfile:
                stm_corr_json = json.dumps(self.new_request['ARGS']['stm_corr_values'], indent=4)
                outfile.write(stm_corr_json)

            with open(request.get('ARGS').get('stm_reconstructed_data_path'), "w") as outfile:
                stm_rcnst_json = json.dumps(self.new_request['ARGS']['stm_graphs'], indent=4)
                outfile.write(stm_rcnst_json)

            super().handle(self.new_request)

        else:
            return super().handle(request)

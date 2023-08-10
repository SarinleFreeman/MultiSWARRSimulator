import json
from copy import copy


from src.SingleInstance.Capacity.CapacityCalculations.Definition.CapacityCalculator.builder import \
    CapacityCalculatorBuilder
from src.SingleInstance.Capacity.CapacityCalculations.Definition.CapacityCalculator.definition import \
    calculate_corr_coefs
from src.SingleInstance.Capacity.CapacityCalculations.STM.definition import gen_y_stm
from src.Utils.DataParser.definition import DataParser
from src.Utils.Handler.definition import AbstractHandler


class TransientHandler(AbstractHandler):
    def __init__(self: 'TransientHandler', next_step='PC_CALC'):
        self.next_step = next_step
        self.new_request = None
        self.name = 'STM_CALC'

    def get_output(self):
        return self.new_request

    def handle(self: 'TransientHandler', request: dict) -> None:
        if request.get('TYPE') == self.name:
            # build calculator
            dp = DataParser(self.args.get('sim_path'), self.args.get('output_antannae'))
            dp.load_data()
            transient_time = dp.get_transient_time()


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

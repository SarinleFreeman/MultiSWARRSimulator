from numpy import asarray, ndarray

from src.SingleInstance.Capacity.CapacityCalculations.Definition.CapacityCalculator.definition import CapacityCalculator


class STMCapacityCalculator(CapacityCalculator):
    def transform_data(self, max_delay: int):
        # Transform x by removing the first `max_delay` elements
        x_transformed = self.splt_amps[max_delay:]

        # Transform y by creating a matrix of delayed versions of y
        y_transformed = gen_y_stm(max_delay=max_delay,y=self.av_splt_bins)

        self.splt_amps = asarray(x_transformed)
        self.av_splt_bins = asarray(y_transformed)


def gen_y_stm(max_delay: int, y: ndarray) -> ndarray:
    y_transformed = []
    for i in range(max_delay + 1):
        start_idx = max_delay - i
        end_idx = start_idx + len(y) - max_delay
        y_short = y[start_idx:end_idx]
        y_transformed.append(y_short)
    return asarray(y_transformed)

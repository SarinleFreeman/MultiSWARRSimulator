from abc import ABC

from numpy import asarray, ndarray

from src.Capacity.CapacityCalculations.Definition.CapacityCalculator.definition import CapacityCalculator


class PCCapacityCalculator(CapacityCalculator):
    def transform_data(self, max_delay):
        # ignore delays
        x_transformed = self.splt_amps[max_delay:]
        y_transformed = gen_y_pc(max_delay=max_delay, y=self.av_splt_bins)

        self.splt_amps = asarray(x_transformed)
        self.av_splt_bins = asarray(y_transformed)


def parity_delay(y, delay):
    y_new = []
    for xx in range(len(y) - delay):
        # For each input xx in y[:-delay] (the last few points are not used)...
        # ...calculate the sum of all points between xx and xx+delay...
        parity = 0
        for ii in range(delay + 1):
            parity += y[xx + ii]
        # ...then take the modulus of that sum and append it to y_new
        y_new.append(divmod(parity, 2)[1])

    return asarray(y_new)


def gen_y_pc(max_delay: int, y: ndarray) -> ndarray:
    y_transformed = []
    for i in range(max_delay + 1):
        y_short = parity_delay(y=y, delay=i)[
                  max_delay - i:max_delay - i + len(y) - max_delay]
        y_transformed.append(y_short)
    return asarray(y_transformed)

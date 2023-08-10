from typing import Tuple

import numpy as np
from numpy import ndarray, asarray, average, corrcoef

from src.SingleInstance.Capacity.CapacityCalculations.Definition.Sampler.definition import SignalSampler
from sklearn.linear_model import LinearRegression
from abc import ABC, abstractmethod


def calculate_corr_coefs(y_pred: ndarray, y: ndarray):
    corr_values = []
    for i in range(len(y_pred)):
        corr_values.append(corrcoef(asarray(y_pred[i]), asarray(y[i]))[0, 1] ** 2)
    return corr_values


class CapacityCalculator(ABC):
    def __init__(self, time_values: ndarray, theta_int: float, output_amps: ndarray, bin_values: ndarray,
                 sampler: SignalSampler):

        # input data
        self.sampler = sampler
        self.output_amps = output_amps
        self.bin_values = bin_values
        self.time_values = time_values
        self.theta_int = theta_int

        # stored data
        self.splt_amps = None
        self.av_splt_bins = None
        self.regressors = None

    def split_data(self, rounder=15):

        # calculate period_length

        if self.theta_int < (self.time_values[1] - self.time_values[0]):
            raise ValueError('Resolution of theta_int is too small, increase your sampling rate!')

        period_length = round(round(self.theta_int, rounder) / (
                round(self.time_values[1], rounder) - round(self.time_values[0], rounder)))


        # get output amps
        self.sampler.fit(self.output_amps, self.time_values)

        splt_amps = self.sampler.split_signal(period_length)

        # get binary amps
        self.sampler.fit(self.bin_values, self.time_values)
        splt_bins = self.sampler.split_signal(period_length)
        av_splt_bins = asarray([average(splt) for splt in splt_bins])

        return splt_amps, av_splt_bins

    def fit_data(self, splt_amps, av_splt_bins):
        self.splt_amps = splt_amps
        self.av_splt_bins = av_splt_bins

    @abstractmethod
    def transform_data(self, max_delay: int):
        pass

    def generate_regressors(self):
        regressors = []
        for y_tau in self.av_splt_bins:
            regressor = LinearRegression()
            regressor.fit(self.splt_amps, y_tau)
            regressors.append(regressor)

        self.regressors = regressors

    def predict(self, x: ndarray):

        y_predictions = []
        for regressor in self.regressors:
            y_predictions.append(regressor.predict(x))
        return asarray(y_predictions)

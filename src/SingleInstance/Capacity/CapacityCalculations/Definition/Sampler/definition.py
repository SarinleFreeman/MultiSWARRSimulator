class SignalSampler:

    def __init__(self, signal_values=None, times=None):
        self.signal_values = signal_values
        self.times = times

    def split_signal(self, period_length:float):
        # Calculate the number of complete periods that can be obtained from the signal
        num_periods = len(self.signal_values) // period_length


        #raise exception if period length is larger than the sample run time.c
        if num_periods < 1:
            raise ValueError("Period length must not exceed signal length")
        # Truncate the signal to an integer multiple of the period length
        truncated_signal = self.signal_values[:num_periods * period_length]


        # Reshape the truncated signal into a matrix, where each row represents a period
        periods = truncated_signal.reshape(num_periods, period_length)

        # Return the periods as a 2D array
        return periods

    def fit(self,signal_values,times):
        self.signal_values = signal_values
        self.times = times

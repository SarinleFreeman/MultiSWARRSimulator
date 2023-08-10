from numpy import random, array, pi, exp


class Amplifier:
    def __init__(self, gain: float, noise_floor: float):
        """
        Initialize the Amplifier class with gain and noise floor values
        :param gain: float value representing the gain of the amplifier
        :param noise_floor: float value representing the noise floor of the amplifier
        """
        self.gain = gain
        self.noise_floor = noise_floor

    def amplify(self, value: array) -> array:
        """
        Amplify the input signal with the gain and noise floor values
        :param value: numpy array representing the input signal
        :return: numpy array representing the amplified signal
        """
        phase = random.uniform(-pi, pi)  # generate a random phase between -pi and pi

        return self.gain * exp(1j*phase)*(value + self.noise_floor * (random.random(value.shape)))

    def set_gain(self, gain: float) -> None:
        """
        Set the gain value of the amplifier
        :param gain: float value representing the new gain
        :return: None
        """
        self.gain = gain

    def set_noise_floor(self, noise_floor: float) -> None:
        """
        Set the noise floor value of the amplifier
        :param noise_floor: float value representing the new noise floor
        :return: None
        """
        self.noise_floor = noise_floor

    def get_gain(self) -> float:
        """
        Get the current gain value of the amplifier
        :return: float value representing the current gain
        """
        return self.gain

    def get_noise_floor(self) -> float:
        """
        Get the current noise floor value of the amplifier
        :return: float value representing the current noise floor
        """
        return self.noise_floor

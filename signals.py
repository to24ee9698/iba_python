""" A module that defines generators for signals used for testing and demonstrations."""

import random
import math
from itertools import count


def sinusoid(amplitude, period, phase=0, offset=0, signal_to_noise_ratio=1000):
    """ A function that generates a sinusoid signal with random noise added.

    Args:
        amplitude: Amplitude of the sinusoid
        period:  Period of the sinusoid
        phase: The phase shift of the sinusoid.
        offset: The amount the signal is offset from 0
        signal_to_noise_ratio: The amount of noise added to the base signal.

    Yields:
        A sinusoid signal

    """
    random.seed()
    period_counter = 0
    for item in count(1):
        period_counter += 1
        value = amplitude * math.sin(item * (period_counter / period) + phase)
        yield  value + value * (1/signal_to_noise_ratio) * random.random()


def digital(amplitude, period, offset=0, signal_to_noise_ratio=1000):
    """ A function that generates a digital signal with random noise added.

    Args:
        amplitude: Amplitude of the digital signal
        period: Period of the digital signal
        offset: The amount the signal is offset from 0
        signal_to_noise_ratio: The amount of noise added to the base signal.

    Yields:
        A digital signal with noise added.

    """
    random.seed()
    period_counter = 0
    for item in count(1):
        if period_counter < period:
            period_counter += 1
            yield amplitude * (1 / signal_to_noise_ratio) * random.random() + offset
        elif period_counter < 2 * period:
            period_counter += 1
            yield amplitude + amplitude * (1 / signal_to_noise_ratio) * random.random() + offset
        else:
            period_counter = 0


def white_noise(amplitude):
    """ Produces a random signal times the amplitude. Uses random() function to generate a number between 0.0 and 1.0

    Args:
        amplitude: The amplitude of the signal

    Yields:
        A random signal.

    """
    for item in count(1):
        yield amplitude * random.random()


if __name__ =='__main__':
    gen = white_noise(50)
    for i in range(100):
        print(next(gen))
""" Defines an abstract strategy class, which will allow different processing for different derived classes
    of this base class.  """
from abc import ABCMeta, abstractmethod


class AbsStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, value):
        """ An abstract method that will do special processing for each type of object received.

            Args:
                value: An object that is passed from the calling class for processing in this class.

            Returns:
                None

            Raises:
                None
        """
        pass

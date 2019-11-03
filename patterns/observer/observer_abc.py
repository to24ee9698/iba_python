""" An abstract Observer class used in the subject-observer pattern by the
    G.o.F book - "Design Patterns - Elements of reusable software."
"""
import abc


class AbsObserver(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def update(self, value):
        """ A abstract method that is implemented by derived classes, which is called by a concrete class
            derived from AbsSubject when the concrete class has been changed.

            Args:
                value: An object that is passed from the subject for processing.

            Returns:
                None

            Raises:
                None
        """
        pass

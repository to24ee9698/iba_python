""" An abstract Subject class used in in the subject-observer pattern by the
    G.o.F book - "Design Patterns - Elements of reusable software. "
"""
import abc
from patterns.observer.observer_abc import AbsObserver


class AbsSubject(object):
    __metaclass__ = abc.ABCMeta
    _observers = set()

    def attach(self, observer):
        """ Attach an observer object to this subject.

            Args:
                observer: The observer to that will be notified when this subject changes.

            Returns:
                None

            Raises:
                TypeError: If the observer object passed is not derived from AbsObserver.
        """
        if not isinstance(observer, AbsObserver):
            raise TypeError('Observer not derived from AbsObserver')
        self._observers |= {observer}

    def detach(self, observer):
        """ Detach an observer object watching this subject.

            Args:
                observer: The observer to that will be removed from the list of notified objects when
                this subject changes.

            Returns:
                None

            Raises:
                None
        """
        self._observers -= {observer}

    def notify(self, value=None):
        """ Notify the list of all observer objects watching this subject.

            Args:
                value: An object that is passed to the observer for processing.

            Returns:
                None

            Raises:
                None
        """
        for observer in self._observers:
            observer.update(value)

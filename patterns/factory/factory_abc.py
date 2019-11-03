import abc


class AbsFactory(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_instance(self, value):
        pass

    @staticmethod
    def load_factory(factory_name, null_name, products):
        pass

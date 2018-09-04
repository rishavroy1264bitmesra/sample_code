import abc
import logging

logger = logging.getLogger(__name__)


class AbstractValidator(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def validate(self, dataframe):
        return dataframe

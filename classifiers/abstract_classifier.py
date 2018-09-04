import abc
import inspect
import logging
import os

logger = logging.getLogger(__name__)

class AbstractClassifier(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def train(self, train_folder):
        pass

    @abc.abstractmethod
    def classify_dataframe(self, dataframe):
        pass

    def get_model_path(self, client_name, model_name):
        return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
                            '../models/' + client_name + '/' + model_name + '.pkl')

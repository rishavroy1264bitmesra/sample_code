import abc


class AbstractJSONGenerator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getJSON_using_dataframes(self):
        pass

    @abc.abstractmethod
    def generate_json(self):
        pass

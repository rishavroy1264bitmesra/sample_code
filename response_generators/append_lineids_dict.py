__author__ = 'Rishav'
from response_generators.abstract_json_generator import AbstractJSONGenerator
from src.bullet_detector import BulletsDetector
from utils.generator_utils import GeneratorUtils
from utils.tags import Tag


class LineIdsDictionaryJSONGenerator(AbstractJSONGenerator):
    '''Class responsible for generation of JSON Response for Paragraphs, Not Logging anything, if bug comes Please debug using pycharm debugger.'''

    def __init__(self):
        self.util = GeneratorUtils()
        self.bullet_detector = BulletsDetector()

    def getJSON_using_dataframes(self, dataframes):
        paragraphs = dict()
        for dataframe in dataframes:
            output = self.generate_json(dataframe)
            paragraphs.update(output)
        return paragraphs

    def generate_json(self, df):
        output = dict()
        for index, row in df.iterrows():
            text = row[Tag.TEXT.value]
            line_id = row['Tag_no']
            output[line_id] = text
        return output

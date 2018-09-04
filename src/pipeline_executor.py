import json
import logging
import os
import time
from os.path import basename

from response_generators.flat_json_generator import FlatJSONGenerator
from src.classifiers_executor import RunClassifiers
from src.html_gen_executor import HTMLGeneratorRunner
from src.html_line_parser import HTMLReader
from src.html_splitter import HTMLSplitter
from src.json_gen_executor import JSONGeneratorRunner
from src.validators_executor import RunValidators

logger = logging.getLogger(__name__)


class Executor(object):
    def __init__(self, client_name):
        self.client_name = client_name
        self.classifier = RunClassifiers(client_name)

    def execute(self, data):
        splitter = HTMLSplitter()
        parser = HTMLReader()
        validator = RunValidators()
        dict_of_files, file_names = splitter.split_input_file(data)
        documents_dfs = parser.get_doc_as_dataframes(dict_of_files, file_names)
        results = list()
        for document_df in documents_dfs:
            classified_dataframe = self.classifier.run_classifier(document_df.parsed_dataframe)
            validated_dataframe = validator.run_validator(classified_dataframe)
            document_df.parsed_dataframe = validated_dataframe
            results.append(document_df)
        logger.info("Successfully Classified Layouts.")
        return results

    def flatresponse(self, data):
        start = time.time()
        documents_dfs = self.execute(data)
        generator = FlatJSONGenerator()
        dataframes = [document_df.parsed_dataframe for document_df in documents_dfs]
        output = generator.getJSON_using_dataframes(dataframes)
        logger.info("Successfully Generated Flat JSON Response")
        stop = time.time()
        logger.info("Total Response time %s seconds", (stop - start))
        return output

    def normalresponse(self, data):
        start = time.time()
        generator = JSONGeneratorRunner()
        documents_dfs = self.execute(data)
        dataframes = [document_df.parsed_dataframe for document_df in documents_dfs]
        output = generator.run_generators(dataframes)
        logger.info("Successfully Generated Normal JSON Response")
        stop = time.time()
        logger.info("Total Response time %s seconds", (stop - start))
        return output

    def htmlresponse(self, data):
        start = time.time()
        generator = HTMLGeneratorRunner()
        documents_dfs = self.execute(data)
        dataframes = [document_df.parsed_dataframe for document_df in documents_dfs]
        output = generator.run_html_generators(dataframes,data)
        logger.info("Successfully Generated Normal HTML Response")
        stop = time.time()
        logger.info("Total Response time %s seconds", (stop - start))
        return output

    def sub_section_lineids_response(self, data):
        start = time.time()
        generator = JSONGeneratorRunner()
        documents_dfs = self.execute(data)
        dataframes = [document_df.parsed_dataframe for document_df in documents_dfs]
        output = generator.run_lineids_generator(dataframes)
        logger.info("Successfully Generated Normal JSON Response")
        stop = time.time()
        logger.info("Total Response time %s seconds", (stop - start))
        return output

    def dump_json_response(self, output, file):
        file_path = os.path.join(os.path.dirname(file), basename(file).replace('.', '_') + '_output.json')
        with open(file_path, 'w') as outfile:
            outfile.write(output)
        return json.dumps({'file_path': file_path}, indent=4)

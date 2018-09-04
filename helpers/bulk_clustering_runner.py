import logging
import time
from os.path import basename


from classifiers.layout_classifier import LayoutClassifier
from helpers.abstract_bulk_runner import AbstractBulkRunner
from src.html_docs_parser import HTMLReader
from src.html_splitter import HTMLSplitter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BulkClusteringRunner(AbstractBulkRunner):
    def __init__(self):
        self.classifier = LayoutClassifier()

    def run_clustering_and_classification_pipeline(self, data):
        start = time.time()
        splitter = HTMLSplitter()
        parser = HTMLReader()
        logger.debug("Splitting HTML file to multiple HTML files, based on document type.")
        dict_of_files, file_names = splitter.split_input_file(data)
        logger.debug("Successfully splitted into %s HTML files.", len(file_names))
        logger.debug("Starting Clustering for Document")
        dataframes = parser.get_doc_as_dataframes(dict_of_files, file_names)
        clustered_results = list()
        final_result = list()
        for dataframe in dataframes:
            clustered_results.append(self.clustering.cluster_dataframe(dataframe))
        logger.debug("Successfully Clustered Layouts.")
        logger.debug("Starting Classification for Document")
        for dataframe in clustered_results:
            final_result.append(self.classifier.classify_dataframe(dataframe))
        logger.debug("Successfully Completed Classification.")
        stop = time.time()
        logger.debug("Total Response time %s seconds", (stop - start))
        return dataframes

    def executor(self, folder_path):
        to_run = True
        while (to_run):
            successful = list()
            try:
                start = time.time()
                for file in self.read_all_train_files(folder_path):
                    with open(file, mode='r', encoding='ISO-8859-1') as in_file:
                        data = in_file.read()
                    result_dataframes = self.run_clustering_and_classification_pipeline(data)
                    self.write_dataframes_to_excel(result_dataframes, folder_path, basename(file))
                    # self.write_json_output(folder_path, output, basename(file))
                    successful.append(file)
                print("Total time: ", (time.time() - start), " seconds")
                to_run = False
            except:
                print("Error in File: ", basename(file))
                self.write_failure_files(file, folder_path)
                self.move_successful(successful, folder_path)
                to_run = True


if __name__ == '__main__':
    runner = BulkClusteringRunner()
    runner.executor('C:\\Users\\RI386799\\Downloads\\pdf_run_output\\ocr_corrected')

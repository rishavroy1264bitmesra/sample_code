import time
from os.path import basename

from helpers.abstract_bulk_runner import AbstractBulkRunner
from src.classifiers_executor import RunClassifiers
from src.html_line_parser import HTMLReader
from src.html_splitter import HTMLSplitter
from utils.tags import Tag


class TrainDatasetGenerator(AbstractBulkRunner):
    def executor(self, folder_path, client_name):
        to_run = True
        start = time.time()
        while (to_run):
            successful = list()
            try:
                for file in self.read_all_train_files(folder_path):
                    with open(file, mode='r', encoding='ISO-8859-1') as in_file:
                        data = in_file.read()
                    reader = HTMLReader()
                    splitter = HTMLSplitter()
                    classifier_executor = RunClassifiers(client_name=client_name)
                    splitted_files, file_names = splitter.split_input_file(data)
                    unit_docs = reader.get_doc_as_dataframes(splitted_files, file_names)
                    print("Splitted Documents Size: ", len(file_names))
                    count = 0
                    for unitdoc in unit_docs:
                        count += 1
                        classified_df = classifier_executor.run_classifier(unitdoc.parsed_dataframe)
                        self.write_dataframe_to_excel(classified_df, 'Sheet1', folder_path,
                                                      basename(file) + '_' + str(count) + '_.xlsx')
                    print("Completed Training File Generation")
                    successful.append(file)
                to_run = False
            except Exception as e:
                print(e)
                print("Error in File: ", basename(file))
                self.write_failure_files(file, folder_path)
                self.move_successful(successful, folder_path)
                to_run = True
        print("Total time: ", (time.time() - start), " seconds")
        print("Unable to process : ", self.failure)
        print("Able to process : ", self.success)


if __name__ == '__main__':
    train_generator = TrainDatasetGenerator()
    train_generator.executor('C:\\Users\\RI386799\\Documents\\test_final_atnt\\dtu_processed_bk', Tag.T_MOBILE.value)

import time
import os
from os.path import basename,join
from helpers.abstract_bulk_runner import AbstractBulkRunner
from src.pipeline_executor import Executor
from utils.tags import Tag


class BulkClassificationRunner(AbstractBulkRunner):

    def executor(self, folder_path, client_name):
        to_run = True
        while (to_run):
            successful = list()
            try:
                start = time.time()
                for file in self.read_all_train_files(folder_path):
                    with open(file, mode='r', encoding='ISO-8859-1') as in_file:
                        data = in_file.read()
                    executor = Executor(client_name=client_name)
                    output = executor.sub_section_lineids_response(data)
                    self.write_json_output(folder_path, output, basename(file))
                    successful.append(file)
                print("Total time: ", (time.time() - start), " seconds")
                to_run = False
            except Exception as e:
                print("Error in File: ", basename(file))
                print(e.with_traceback())
                self.write_failure_files(file, folder_path)
                self.move_successful(successful, folder_path)
                to_run = True
        print("Unable to process : ", self.failure)
        print("Able to process : ", self.success)

    def process_files(self, folder_name, client_name, dtu_processed_folder_present=False):
        if dtu_processed_folder_present:
            folder_name=os.path.join(folder_name, 'dtu_processed')
        extractor_helper = BulkClassificationRunner()
        extractor_helper.executor(folder_name, client_name)

    def process_files_in_subdirectories(self, root_folder, client_name, dtu_processed_folder_present=False):
        for folder in self.read_all_directories(root_directory=root_folder):
            if dtu_processed_folder_present:
                folder = os.path.join(folder, 'dtu_processed')
            extractor_helper = BulkClassificationRunner()
            extractor_helper.executor(folder, client_name)


if __name__ == '__main__':
    folder = "D:\Lease_Agreements\htmls\dtu_processed"
    client_name = Tag.T_MOBILE.value
    classifer_helper = BulkClassificationRunner()
    classifer_helper.process_files(folder_name=folder, client_name=client_name,dtu_processed_folder_present=False)
    #classifer_helper.process_files_in_subdirectories(root_folder=folder, client_name=client_name,
    #                                                 dtu_processed_folder_present=True)

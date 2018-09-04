import os
import time
from os.path import basename

import requests

from helpers.abstract_bulk_runner import AbstractBulkRunner

DTU_PROCESSED = 'DTU'
HTML_EXTENSION = '.html'


class BulkDoctypeRunner(AbstractBulkRunner):
    def executor(self, folder_path, doc_type_endpoint):
        to_run = True
        index = 0
        while (to_run):
            successful = list()
            try:
                start = time.time()
                for file in self.read_all_train_files(folder_path):
                    if not file.endswith('.html'):
                        raise Exception("File Format Not Supported: " + basename(file))
                    with open(file, mode='r', encoding='ISO-8859-1') as in_file:
                        data = in_file.read()
                    self.post_and_write(data, doc_type_endpoint, basename(file), folder_path)
                    successful.append(file)
                    index += 1
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

    def post_and_write(self, data, end_point, filename, folder_path):
        response = requests.post(url=end_point, data=data)
        output_folder = os.path.join(folder_path, 'dtu_processed')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if response.status_code == 200:
            output_file = os.path.join(output_folder, filename + DTU_PROCESSED + HTML_EXTENSION)
            with open(output_file, mode='w', encoding='utf-8') as to_write:
                to_write.write(response.text)
        else:
            raise ConnectionError("Unable to get response")

    def process_files(self, folder_name, url):
        extractor_helper = BulkDoctypeRunner()
        extractor_helper.executor(folder_name, url)

    def process_files_in_subdirectories(self, root_folder, url):
        for folder in self.read_all_directories(root_directory=root_folder):
            extractor_helper = BulkDoctypeRunner()
            extractor_helper.executor(folder, url)


if __name__ == '__main__':
    folder = "D:\Lease_Agreements\htmls"
    url = "http://10.210.16.129:8091/holmes4business/contract_intel/v1/IdentifyDocType"
    extractor_helper = BulkDoctypeRunner()
    extractor_helper.process_files(folder_name=folder, url=url)
    #extractor_helper.process_files_in_subdirectories(root_folder=folder, url=url)

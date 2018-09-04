import os
import time
from os.path import basename

import requests

from helpers.abstract_bulk_runner import AbstractBulkRunner

OCR_PROCESSED = 'OCR'
HTML_EXTENSION = '.html'
OCR_API = ''


class BulkOcrRunner(AbstractBulkRunner):
    def executor(self, folder_path, ocr_endpoint):
        to_run = True
        index = 0
        while (to_run):
            successful = list()
            try:
                start = time.time()
                for file in self.read_all_train_files(folder_path):
                    with open(file, mode='rb') as in_file:
                        self.post_and_write(in_file, ocr_endpoint, basename(file), folder_path)
                    successful.append(file)
                    index += 1
                print("Total time: ", (time.time() - start), " seconds")
                to_run = False
            except Exception as e:
                print("Error in File: ", basename(file))
                print(e)
                self.write_failure_files(file, folder_path)
                self.move_successful(successful, folder_path)
                to_run = True
        print("Unable to process : ", self.failure)
        print("Able to process : ", self.success)

    def post_and_write(self, file, end_point, filename, folder_path):
        response = requests.post(url=end_point, files={'file': file})
        output_folder = os.path.join(folder_path, 'ocr_processed')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        if response.status_code == 200:
            output_file = os.path.join(output_folder, filename + OCR_PROCESSED + HTML_EXTENSION)
            with open(output_file, mode='w', encoding='utf-8') as to_write:
                to_write.write(response.text)
        else:
            raise ConnectionError("Unable to get response")


if __name__ == '__main__':
    folder = "C:\\Users\\RI386799\\Documents\\atnt_ocr"
    extractor_helper = BulkOcrRunner()
    extractor_helper.executor(folder, "http://10.210.16.129:8087/")

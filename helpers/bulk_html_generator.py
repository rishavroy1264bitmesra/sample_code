import time
from os.path import basename

from helpers.abstract_bulk_runner import AbstractBulkRunner
from src.pipeline_executor import Executor
from utils.tags import Tag


class BulkHTMLGeneratorRunner(AbstractBulkRunner):
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
                    output = executor.htmlresponse(data)
                    self.write_html_output(folder_path, output, basename(file))
                    successful.append(file)
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


if __name__ == '__main__':
    folder = "D:\EERM_Data\htmls_docType"
    classifer_helper = BulkHTMLGeneratorRunner()
    classifer_helper.executor(folder, client_name=Tag.ERM.value)

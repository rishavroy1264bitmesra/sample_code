import json
import time
from os.path import basename

import pandas as pd

from helpers.abstract_bulk_runner import AbstractBulkRunner
from src.pipeline_executor import Executor
from utils.tags import Tag


class BulkDocumentTitleExtractor(AbstractBulkRunner):
    def __init__(self):
        self.success = 0
        self.failure = 0
        self.columns = ['file_name', 'attribute_name', 'attribute_value', 'document_type', 'priority', 'line_id',
                        'page_number']
        self.dataframe = pd.DataFrame(columns=self.columns)

    def update_dataframe(self, json_input, index, file_name):
        dict_inp = json.loads(json_input)
        doc_titles = dict_inp.get('Document_Titles')
        attribute_name = ''
        attribute_value = ''
        document_type = ''
        priority = ''
        line_id = ''
        page_number = ''
        for title in doc_titles:
            attribute_name = title.get('attribute_name')
            attribute_value = title.get('attribute_value')
            document_type = title.get('document_type')
            priority = title.get('priority')
            line_id = title.get('line_id')
            page_number = title.get('page_number')
            break
        self.dataframe.loc[index] = [file_name, attribute_name, attribute_value, document_type, priority, line_id,
                                     page_number]

    def executor(self, folder_path, client_name):
        to_run = True
        index = 0
        while (to_run):
            successful = list()
            try:
                start = time.time()
                for file in self.read_all_train_files(folder_path):
                    with open(file, mode='r', encoding='ISO-8859-1') as in_file:
                        data = in_file.read()
                    executor = Executor(client_name=client_name)
                    output = executor.normalresponse(data)
                    self.update_dataframe(output, index, basename(file))
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
        self.write_dataframe_to_excel(self.dataframe, 'Extracted_DocTitles', folder_path, 'identifies_doc_titles.xlsx')


if __name__ == '__main__':
    folder = "D:\\Updated_OCR_DOCUMENTS\\T-Mobile_tess_4_dtu\\T-Mobile_tess_4_dtu"
    extractor_helper = BulkDocumentTitleExtractor()
    extractor_helper.executor(folder, client_name=Tag.T_MOBILE.value)

from os.path import dirname, basename

import pandas as pd
import json
from classifiers.layout_classifier import LayoutClassifier
from helpers.abstract_bulk_runner import AbstractBulkRunner


class ClassifierRunner(AbstractBulkRunner):
    def executor(self, excel_file_path):
        classifier = LayoutClassifier()
        df = pd.read_excel(open(excel_file_path, mode='rb'), sheetname='Sheet1')
        output = classifier.classify_dataframe(df)
        self.write_dataframe_to_excel(output, 'Sheet1', dirname(excel_file_path),
                                      basename(excel_file_path) + '_classified_para.xlsx')


if __name__ == '__main__':
    reader = ClassifierRunner()
    files = reader.read_all_train_files(
        'D:\\Updated_OCR_DOCUMENTS\T-Mobile_tess_4_dtu\T-Mobile_tess_4_dtu\generated_output')
    for file in files:
        with open(file, mode='r') as infile:
            data = infile.read()
        dict_inp = json.loads(data)
        doc_titles = dict_inp.get('Document_Titles')
        for title in doc_titles:
            print(title.get('attribute_value'))
        print('-----------------------------------')

import importlib
import logging
import os
import time
from os import listdir
from os.path import isfile, join

import pandas as pd
import sklearn_crfsuite
from sklearn_crfsuite import metrics

from utils.model_loader import LAYOUT_MODELS
from utils.model_loader import load_all_models
from utils.tags import Tag

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Evaluator(object):
    def __init__(self, dataset, model):
        try:
            path = '../datasets/' + dataset
            load_all_models(model)
            self.test_path = os.path.join(path, 'test')
            print(self.test_path)
            self.dataset = dataset
            self.classifier = sklearn_crfsuite.CRF(algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=200,
                                                   all_possible_transitions=True)
            self.client_name = model
            self.module_name = 'feature_extractors.' + self.client_name + '_layout_feature_extractor_crf'
            self.classifier = LAYOUT_MODELS.get(model)
        except Exception:
            raise FileNotFoundError("Caught Exception in getting loaded model")

    def read_all_train_files(self, folder_path):
        onlyfiles = [os.path.join(folder_path, f) for f in listdir(folder_path) if
                     isfile(join(folder_path, f))]
        return onlyfiles

    def classify_dataframe(self):
        x_tests = list()
        y_tests = list()
        classes = list(self.classifier.classes_)
        logger.debug("Using Conditional Random Fields for Layout Classification")
        my_module = importlib.import_module(self.module_name)
        FeatureExtractor = getattr(my_module, "FeatureExtractor")
        f_extractor = FeatureExtractor()
        for file in self.read_all_train_files(self.test_path):
            file_df = pd.read_excel(open(file, mode='rb'), sheetname='Sheet1')
            file_texts = list()
            file_labels = list()
            for index, row in file_df.iterrows():
                file_texts.append(row[Tag.TEXT.value])
                file_labels.append(row[Tag.TAG.value])
            file_features = f_extractor.extract_features(file_texts, 7, 7)
            x_tests.append(file_features)
            y_tests.append(file_labels)
        y_predict = self.classifier.predict(x_tests)
        eval_score = metrics.flat_classification_report(y_tests, y_predict, labels=classes, digits=3)
        print(eval_score)
        self.eval_score_writer(eval_score=eval_score)
        return None

    def eval_score_writer(self, eval_score):
        separator = '-' * 100
        text = separator + '\n' + time.asctime() + '\n' + eval_score
        with open('../datasets/' + self.dataset + '/' + self.client_name + '_layout_model_eval.txt', 'a') as out_file:
            out_file.write(text)


if __name__ == '__main__':
    dataset = Tag.T_MOBILE.value
    model = Tag.GENERIC.value
    evaluator = Evaluator(dataset=dataset, model=model)
    evaluator.classify_dataframe()

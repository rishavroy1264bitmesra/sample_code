import importlib
import logging
import os
import time
from os import listdir
from os.path import isfile, join

import pandas as pd
import sklearn_crfsuite
from sklearn.externals import joblib
from sklearn_crfsuite import metrics

from classifiers.abstract_classifier import AbstractClassifier
from utils.model_loader import LAYOUT_MODELS
from utils.tags import Tag

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CRFLayoutClassifier(AbstractClassifier):
    def __init__(self, client_name):
        try:
            self.classifier = sklearn_crfsuite.CRF(algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=200,
                                                   all_possible_transitions=True)
            self.client_name = client_name
            self.module_name = 'feature_extractors.' + self.client_name + '_layout_feature_extractor_crf'
            self.classifier_model = LAYOUT_MODELS.get(client_name)
        except Exception:
            raise FileNotFoundError("Caught Exception in getting loaded model")

    def read_all_train_files(self, folder_path):
        onlyfiles = [os.path.join(folder_path, f) for f in listdir(folder_path) if
                     isfile(join(folder_path, f))]
        return onlyfiles

    def train(self, folder_path, preceding=0, following=0):
        logger.info("Starting Model Training, using training files from %s", folder_path)
        train_path = os.path.join(folder_path, 'train')
        test_path = os.path.join(folder_path, 'test')
        if not os.path.exists(train_path) or not os.path.exists(test_path):
            raise ValueError("Either of the train/test folders doesn't exists")
        features = list()
        labels = list()
        start = time.time()
        my_module = importlib.import_module(self.module_name)
        FeatureExtractor = getattr(my_module, "FeatureExtractor")
        feature_extractor = FeatureExtractor()
        for file in self.read_all_train_files(train_path):
            file_df = pd.read_excel(open(file, mode='rb'), sheetname='Sheet1')
            file_texts = list()
            file_labels = list()
            for index, row in file_df.iterrows():
                file_texts.append(row[Tag.TEXT.value])
                file_labels.append(row[Tag.TAG.value])
            file_features = feature_extractor.extract_features(file_texts, preceding, following)
            features.append(file_features)
            labels.append(file_labels)
        stop = time.time()
        logger.info("Feature Extraction Completed for training file in %s seconds.Starting Model Training",
                    (stop - start))
        start = time.time()
        logger.info("Features: %s", len(features))
        logger.info("Labels: %s", len(labels))
        self.classifier.fit(features, labels)
        stop = time.time()
        logger.info("Completed Model Training in %s seconds.", (stop - start))
        model_path = self.get_model_path(client_name=self.client_name, model_name='layout_classifier_model_crf')
        joblib.dump(self.classifier, model_path)
        logger.info("Writing model to path: %s", model_path)
        classes = list(self.classifier.classes_)
        x_tests = list()
        y_tests = list()
        for file in self.read_all_train_files(test_path):
            file_df = pd.read_excel(open(file, mode='rb'), sheetname='Sheet1')
            file_texts = list()
            file_labels = list()
            for index, row in file_df.iterrows():
                file_texts.append(row[Tag.TEXT.value])
                file_labels.append(row[Tag.TAG.value])
            file_features = feature_extractor.extract_features(file_texts, preceding, following)
            x_tests.append(file_features)
            y_tests.append(file_labels)
        y_predict = self.classifier.predict(x_tests)
        eval_score = metrics.flat_classification_report(y_tests, y_predict, labels=classes, digits=3)
        print(eval_score)
        self.eval_score_writer(eval_score=eval_score)

    def classify_dataframe(self, dataframe):
        try:
            logger.debug("Using Conditional Random Fields for Layout Classification")
            my_module = importlib.import_module(self.module_name)
            FeatureExtractor = getattr(my_module, "FeatureExtractor")
            f_extractor = FeatureExtractor()
            texts = list()
            for index, row in dataframe.iterrows():
                texts.append(row[Tag.TEXT.value])
            x_features = f_extractor.extract_features(texts, 7, 7)
            classified_results = self.classifier_model.predict_single(x_features)
            dataframe.insert(loc=1, column='Tag', value=classified_results)
        except Exception:
            raise ValueError("Error occured while Layout Classification")
        return dataframe

    def eval_score_writer(self, eval_score):
        separator = '-' * 100
        text = separator + '\n' + time.asctime() + '\n' + eval_score
        with open('../datasets/' + self.client_name + '/' + self.client_name + '_layout_model_eval.txt',
                  'a') as out_file:
            out_file.write(text)


if __name__ == '__main__':
    client = Tag.T_MOBILE.value
    classifier = CRFLayoutClassifier(client)
    classifier.train('../datasets/' + client, preceding=7, following=7)

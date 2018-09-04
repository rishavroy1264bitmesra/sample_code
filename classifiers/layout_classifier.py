import logging
import os
import time
from os import listdir
from os.path import isfile, join
import importlib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import cross_val_score

from classifiers.abstract_classifier import AbstractClassifier
from utils.tags import Tag

logger = logging.getLogger(__name__)


class LayoutClassifier(AbstractClassifier):
    def __init__(self, client_name):
        try:
            self.feature_vectorizer = DictVectorizer(sparse=False)
            self.classifier = RandomForestClassifier()
            self.client_name = client_name
            self.module_name = 'feature_extractors.' + self.client_name + '_layout_feature_extractor'
            model_path = self.get_model_path(client_name=client_name, model_name='layout_classifier_model')
            vectorizer_path = self.get_model_path(client_name=client_name, model_name='feature_vectorizer')
            self.classifier_model = joblib.load(model_path)
            self.vectorizer_model = joblib.load(vectorizer_path)
            logger.debug("Loaded Model from %s ", model_path)
        except Exception:
            raise FileNotFoundError("Unable to load Layout Classifier models")

    def read_all_train_files(self, folder_path):
        onlyfiles = [os.path.join(folder_path, f) for f in listdir(folder_path) if
                     isfile(join(folder_path, f))]
        return onlyfiles

    def train(self, folder_path):
        logger.debug("Starting Model Training, using training files from %s", folder_path)
        features = list()
        labels = list()
        start = time.time()
        my_module = importlib.import_module(self.module_name)
        FeatureExtractor = getattr(my_module, "FeatureExtractor")
        feature_extractor = FeatureExtractor()
        for file in self.read_all_train_files(folder_path):
            file_df = pd.read_excel(open(file, mode='rb'), sheetname='Sheet1')
            for index, row in file_df.iterrows():
                text = row[Tag.TEXT.value]
                label = row[Tag.TAG.value]
                feature = feature_extractor.extract_features(text)
                features.append(feature)
                labels.append(label)
        stop = time.time()
        logger.debug("Feature Extraction Completed for training file in %s seconds.Starting Model Training",
                     (stop - start))
        start = time.time()
        feature_vectorizer = self.feature_vectorizer.fit_transform(features)
        self.classifier.fit(feature_vectorizer, labels)
        scores = cross_val_score(self.classifier, feature_vectorizer, labels, cv=10)
        print(scores)
        stop = time.time()
        logger.debug("Completed Model Training in %s seconds.", (stop - start))
        model_path = self.get_model_path(client_name=self.client_name, model_name='layout_classifier_model')
        vectorizer_path = self.get_model_path(client_name=self.client_name, model_name='feature_vectorizer')
        joblib.dump(self.classifier, model_path)
        joblib.dump(self.feature_vectorizer, vectorizer_path)
        logger.debug("Writing model to path: %s", model_path)

    def classify_dataframe(self, dataframe):
        try:
            classified_results = list()
            my_module = importlib.import_module(self.module_name)
            FeatureExtractor = getattr(my_module, "FeatureExtractor")
            f_extractor = FeatureExtractor()
            for index, row in dataframe.iterrows():
                x_features = f_extractor.extract_features(row['Text'])
                X = self.vectorizer_model.transform(x_features)
                Y = self.classifier_model.predict(X)
                classified_results.append(Y[0])
            dataframe.insert(loc=1, column='Tag', value=classified_results)
        except Exception:
            raise ValueError("Error occured while Layout Classification")
        return dataframe

    def classify_text(self, text_input):
        start = time.time()
        my_module = importlib.import_module(self.module_name)
        FeatureExtractor = getattr(my_module, "FeatureExtractor")
        f_extractor = FeatureExtractor()
        x_features = f_extractor.extract_features(text_input)
        X = self.vectorizer_model.transform(x_features)
        probablity = self.classifier_model.predict_proba(X)
        Y = self.classifier_model.predict(X)
        stop = time.time()
        logger.debug("Time Taken for Prediction %s seconds", (stop - start))
        logger.debug("Prediction Confidence Score %s ", probablity)
        return Y


if __name__ == '__main__':
    client = 'erm'
    classifier = LayoutClassifier(client)
    classifier.train('../datasets/erm_trainset')
    # classifier.train('../datasets/t_mobile_trainset')
    # classifier.train('../datasets/isda_trainset')

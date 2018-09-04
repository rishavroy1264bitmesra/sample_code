import logging
import os
import time
from os import listdir
from os.path import isfile, join

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import cross_val_score

from classifiers.abstract_classifier import AbstractClassifier
from feature_extractors.document_title_feature_extractor import FeatureExtractor
from utils.model_loader import DOCUMENT_TITLE_CLASSIFIER_MODELS, DOCUMENT_TITLE_VECTORIZER_MODELS
from utils.tags import Tag

logger = logging.getLogger(__name__)


class DocumentTitleeClassifier(AbstractClassifier):
    '''Classifier ,identifies title of the document'''

    def __init__(self, client_name):
        try:
            self.feature_vectorizer = DictVectorizer(sparse=True)
            self.classifier = RandomForestClassifier()
            self.client_name = client_name
            self.classifier_model = DOCUMENT_TITLE_CLASSIFIER_MODELS.get(client_name)
            self.vectorizer_model = DOCUMENT_TITLE_VECTORIZER_MODELS.get(client_name)
        except Exception:
            raise FileNotFoundError("Caught Exception in getting loaded model")

    @staticmethod
    def read_all_train_files(folder_path):
        onlyfiles = [os.path.join(folder_path, f) for f in listdir(folder_path) if
                     isfile(join(folder_path, f))]
        return onlyfiles

    def split_df(self, dataframe, tag_wise_df):
        logger.debug("Splitting pages on basis of %s", tag_wise_df)
        splitted_df = list()
        start = 0
        no_of_pages = 0
        current_page = dataframe[tag_wise_df][0]
        for index, row in dataframe.iterrows():
            if current_page != row[tag_wise_df]:
                splitted_df.append(dataframe[start:index])
                no_of_pages += 1
                start = index
                current_page = row[tag_wise_df]
        splitted_df.append(dataframe[start:])
        no_of_pages += 1
        logger.debug("Found %s different pages, splitted.", no_of_pages)
        return splitted_df

    def train(self, folder_path):
        features = list()
        labels = list()
        start = time.time()
        for file in self.read_all_train_files(folder_path):
            feature_extractor = FeatureExtractor(self.client_name)
            file_df = pd.read_excel(open(file, mode='rb'), sheetname='Sheet1')
            pages = self.split_df(file_df, Tag.PAGE_NUMBER.value)
            for page in pages:
                for index, row in page.iterrows():
                    if index > 5:
                        break
                    text = row[Tag.TEXT.value]
                    document_tile = row[Tag.DOCUMENT_TITLE_LABEL.value]
                    feature = feature_extractor.extract_features(text)
                    features.append(feature)
                    labels.append(document_tile)
        stop = time.time()
        logger.debug("Feature Extraction Completed for training files in %s seconds", (stop - start))
        logger.debug("Starting Model Training")
        start = time.time()
        feature_vectorizer = self.feature_vectorizer.fit_transform(features)
        self.classifier.fit(feature_vectorizer, labels)
        scores = cross_val_score(self.classifier, feature_vectorizer, labels, cv=5)
        print(scores)
        stop = time.time()
        logger.debug("Completed Model Training in %s seconds.", (stop - start))
        model_path = self.get_model_path(client_name=self.client_name, model_name='doc_title_classifier_model')
        vectorizer_path = self.get_model_path(client_name=self.client_name, model_name='doc_title_feature_vectorizer')
        joblib.dump(self.classifier, model_path)
        joblib.dump(self.feature_vectorizer, vectorizer_path)
        logger.debug("Writing model to path: %s", model_path)

    def classify_dataframe(self, dataframe):
        try:
            classified_results = list()
            f_extractor = FeatureExtractor(self.client_name)
            start = time.time()
            pages = self.split_df(dataframe, Tag.PAGE_NUMBER.value)
            for page in pages:
                doc_titles = [Tag.NOT_FOUND.value] * len(page.index)
                count = 0
                for index, row in page.iterrows():
                    if count > 5:
                        break
                    text = row[Tag.TEXT.value]
                    x_features = f_extractor.extract_features(text)
                    X = self.vectorizer_model.transform(x_features)
                    Y = self.classifier_model.predict(X)
                    doc_title_label = str(Y[0])
                    doc_titles[count] = doc_title_label
                    count += 1
                classified_results.extend(doc_titles)
            dataframe.insert(loc=1, column=Tag.DOCUMENT_TITLE_LABEL.value, value=classified_results)
            stop = time.time()
            logger.debug("Completed Document Title Classification in %s seconds", (stop - start))
        except Exception:
            raise ValueError("Error occured while Document Title Classification")
        return dataframe


if __name__ == '__main__':
    type_classifier = DocumentTitleeClassifier(client_name='t_mobile')
    train_folder = "../datasets/t_mobile/train"
    type_classifier.train(train_folder)
    # x = ['h'] * 2
    # print(x)
    # x[1] = 5
    # print(x)

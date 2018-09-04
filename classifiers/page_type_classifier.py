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
from feature_extractors.page_type_feature_extractor import FeatureExtractor
from utils.model_loader import PAGE_TYPE_CLASSIFIER_MODELS,PAGE_TYPE_VECTORIZER_MODELS
from utils.tags import Tag
from validators.page_type_validator import PageTypeValidator

logger = logging.getLogger(__name__)


class PageTypeClassifier(AbstractClassifier):
    '''Classifier , classifies page (Start_Page,TOC_Page and Content_Page) as labels, multiple classes can be added to classify pages within
    a document.'''

    def __init__(self, client_name):
        try:
            self.feature_vectorizer = DictVectorizer(sparse=True)
            self.classifier = RandomForestClassifier()
            self.client_name = client_name
            self.classifier_model = PAGE_TYPE_CLASSIFIER_MODELS.get(client_name)
            self.vectorizer_model = PAGE_TYPE_VECTORIZER_MODELS.get(client_name)
        except Exception:
            raise FileNotFoundError("Caught Exception in getting loaded model")

    @staticmethod
    def read_all_train_files(folder_path):
        onlyfiles = [os.path.join(folder_path, f) for f in listdir(folder_path) if
                     isfile(join(folder_path, f))]
        return onlyfiles

    def split_df_pagewise(self, dataframe):
        pagewise_df = list()
        start = 0
        no_of_pages = 0
        current_page = dataframe['Page_Number'][0]
        for index, row in dataframe.iterrows():
            if current_page != row['Page_Number']:
                pagewise_df.append(dataframe[start:index])
                no_of_pages += 1
                start = index
                current_page = row['Page_Number']
        pagewise_df.append(dataframe[start:])
        no_of_pages += 1
        logger.debug("Found %s different pages, splitted data pagewise.", no_of_pages)
        return pagewise_df

    def train(self, folder_path):
        features = list()
        labels = list()
        start = time.time()
        for file in self.read_all_train_files(folder_path):
            feature_extractor = FeatureExtractor()
            file_df = pd.read_excel(open(file, mode='rb'), sheetname='Sheet1')
            for page_df in self.split_df_pagewise(file_df):
                feature = feature_extractor.extract_features(page_df)
                # text = feature_extractor.convert_to_text(page_df)
                label = page_df.iloc[0][Tag.PAGE_TYPE_LABEL.value]
                features.append(feature)
                labels.append(label)
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
        model_path = self.get_model_path(client_name=self.client_name, model_name='layout_classifier_model')
        vectorizer_path = self.get_model_path(client_name=self.client_name, model_name='feature_vectorizer')
        joblib.dump(self.classifier, model_path)
        joblib.dump(self.feature_vectorizer, vectorizer_path)
        logger.debug("Writing model to path: %s", model_path)

    def classify_dataframe(self, dataframe):
        try:
            classified_results = list()
            f_extractor = FeatureExtractor()
            start = time.time()
            page_validator = PageTypeValidator()
            for page_df in self.split_df_pagewise(dataframe):
                x_features = f_extractor.extract_features(page_df)
                # text = f_extractor.convert_to_text(page_df)
                X = self.vectorizer_model.transform(x_features)
                Y = self.classifier_model.predict(X)
                page_label = str(Y[0])
                page_labels = [page_label] * len(page_df.index)
                page_labels = page_validator.validate(page_labels)
                classified_results.extend(page_labels)
            dataframe.insert(loc=1, column=Tag.PAGE_TYPE_LABEL.value, value=classified_results)
            stop = time.time()
            logger.debug("Completed Page Type Classification in %s seconds", (stop - start))
        except Exception:
            raise ValueError("Error occured while PageType Classification")
        return dataframe

    def write_dataframe_to_excel(self, dataframe, sheet_name, folder_path, file_name):
        destination = os.path.join(folder_path, file_name)
        writer = pd.ExcelWriter(destination)
        dataframe.to_excel(writer, sheet_name)
        writer.save()


if __name__ == '__main__':
    type_classifier = PageTypeClassifier()
    train_folder = "D:\\Datasets\\line_tag_datasets\\page_type_train_data"
    type_classifier.train(train_folder)
    # for file in type_classifier.read_all_train_files("D:\\Datasets\\contracts\\train"):
    #     print("Classifying: ", basename(file))
    #     input_df = pd.read_excel(open(file, mode='rb'), sheetname='Sheet1')
    #     result = type_classifier.predict_page_type(input_df)
    #     type_classifier.write_dataframe_to_excel(result, 'Sheet1', "D:\\Datasets\\contracts\\ml",
    #                                              basename(file) + ".xlsx")

import logging
from utils.model_loader import load_all_models
from classifiers.crf_layout_classifier import CRFLayoutClassifier
from classifiers.document_title_classifier import DocumentTitleeClassifier
from classifiers.page_type_classifier import PageTypeClassifier

logger = logging.getLogger(__name__)


class RunClassifiers(object):
    def __init__(self, client_name):
        load_all_models(client_name)
        self.classifiers = list()
        self.classifiers.append(CRFLayoutClassifier(client_name))
        self.classifiers.append(PageTypeClassifier(client_name))
        self.classifiers.append(DocumentTitleeClassifier(client_name))

    def run_classifier(self, dataframe):
        try:
            for classifier in self.classifiers:
                dataframe = classifier.classify_dataframe(dataframe)
        except Exception as ex:
            logger.error("Caught exception while classification.", exc_info=True)
        return dataframe

import inspect
import logging
import os

from sklearn.externals import joblib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LAYOUT_MODELS = dict()
PAGE_TYPE_VECTORIZER_MODELS = dict()
DOCUMENT_TITLE_VECTORIZER_MODELS = dict()
PAGE_TYPE_CLASSIFIER_MODELS = dict()
DOCUMENT_TITLE_CLASSIFIER_MODELS = dict()


def get_model_path(client_name, model_name):
    return os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
                        '../models/' + client_name + '/' + model_name + '.pkl')


def __load_layout_models(client_name):
    try:
        if client_name not in LAYOUT_MODELS.keys():
            logger.info("Loading Layout Model for Client %s", client_name)
            model_path = get_model_path(client_name=client_name, model_name='layout_classifier_model_crf')
            classifier_model = joblib.load(model_path)
            LAYOUT_MODELS[client_name] = classifier_model
        else:
            logger.debug("Layout Model already loaded for Client %s", client_name)
    except Exception:
        raise FileNotFoundError("Unable to load Layout Classifier models")


def __load_page_type_models(client_name):
    try:
        if client_name not in PAGE_TYPE_VECTORIZER_MODELS.keys() and client_name not in PAGE_TYPE_CLASSIFIER_MODELS.keys():
            logger.info("Loading Page Type Model for Client %s", client_name)
            model_path = get_model_path(client_name=client_name, model_name='page_classifier_model')
            vectorizer_path = get_model_path(client_name=client_name, model_name='page_feature_vectorizer')
            classifier_model = joblib.load(model_path)
            vectorizer_model = joblib.load(vectorizer_path)
            PAGE_TYPE_VECTORIZER_MODELS[client_name] = vectorizer_model
            PAGE_TYPE_CLASSIFIER_MODELS[client_name] = classifier_model
        else:
            logger.debug("Page Type Model already loaded for Client %s", client_name)
    except Exception:
        raise FileNotFoundError("Unable to Load Page Type Classifier models")


def __load_document_title_models(client_name):
    try:
        if client_name not in DOCUMENT_TITLE_VECTORIZER_MODELS.keys() and client_name not in DOCUMENT_TITLE_CLASSIFIER_MODELS.keys():
            logger.info("Loading Document Title Model for Client %s", client_name)
            model_path = get_model_path(client_name=client_name, model_name='doc_title_classifier_model')
            vectorizer_path = get_model_path(client_name=client_name, model_name='doc_title_feature_vectorizer')
            classifier_model = joblib.load(model_path)
            vectorizer_model = joblib.load(vectorizer_path)
            DOCUMENT_TITLE_VECTORIZER_MODELS[client_name] = vectorizer_model
            DOCUMENT_TITLE_CLASSIFIER_MODELS[client_name] = classifier_model
        else:
            logger.debug("Document Title Model already loaded for Client %s", client_name)
    except Exception:
        raise FileNotFoundError("Unable to Load Document Title Classifier models")


def load_all_models(client_name):
    __load_layout_models(client_name)
    __load_page_type_models(client_name)
    __load_document_title_models(client_name)

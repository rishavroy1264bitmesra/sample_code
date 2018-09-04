import logging

from utils.tags import Tag
from validators.abstract_validator import AbstractValidator

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DocTitleValidator(AbstractValidator):
    def __init__(self):
        self.found_start_page = False
        self.found_toc_page = False
        self.found_content_page = False

    def update_found(self, label):
        if label == Tag.CONTENT_PAGE.value:
            self.found_content_page = True
        elif label == Tag.TOC_PAGE.value:
            self.found_toc_page = True
        elif label == Tag.START_PAGE.value:
            self.found_start_page = True

    def validate(self, page_labels):
        logger.debug("Running %s Validator", self.__class__.__name__)
        length = len(page_labels)
        label = page_labels[0]
        result = page_labels
        if label == Tag.START_PAGE.value and (self.found_content_page or self.found_toc_page):
            result = [Tag.CONTENT_PAGE.value] * length
        if label == Tag.TOC_PAGE.value and self.found_content_page:
            result = [Tag.CONTENT_PAGE.value] * length
        self.update_found(label)
        return result

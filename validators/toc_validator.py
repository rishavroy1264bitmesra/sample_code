import logging
import re

from utils.tags import Tag
from validators.abstract_validator import AbstractValidator

logger = logging.getLogger(__name__)


class TOCValidator(AbstractValidator):
    def __init__(self):
        self.toc_pttr = re.compile(r'(\.){4,}', re.IGNORECASE)

    def validate(self, dataframe):
        logger.debug("Running %s Validator", self.__class__.__name__)
        for index, row in dataframe.iterrows():
            if self.is_toc_regex_present(row['Text']):
                dataframe.set_value(index, Tag.TAG.value, Tag.OTHER.value)
        return dataframe

    def is_toc_regex_present(self, text):
        if re.search(self.toc_pttr, text):
            return 1
        else:
            return 0

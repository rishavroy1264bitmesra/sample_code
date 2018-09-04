import copy
import logging

import pandas as pd

from utils.tags import Tag
from validators.abstract_validator import AbstractValidator

logger = logging.getLogger(__name__)

SPECIAL_CHARS = ['.', ':']


class SubHeadingValidator(AbstractValidator):
    def __init__(self):
        self.to_insert = list()

    def validate(self, dataframe):
        logger.debug("Running %s Validator", "SubHeadingValidator")
        try:
            df = pd.DataFrame()
            frames = dataframe.to_dict(orient='records')
            for row in frames:
                break_point = -1
                text = row['Text']
                tag = row['Tag']
                if tag == Tag.SUB_HEADING.value:
                    break_point = self.check_if_has_specialchar(text)
                if break_point == -1:
                    df = df.append(self.get_row_dict(row, text, tag), ignore_index=True)
                else:
                    subheading_text = text[:break_point + 1]
                    para_text = text[break_point + 1:]
                    df = df.append(self.get_row_dict(row, subheading_text, Tag.SUB_HEADING.value), ignore_index=True)
                    df = df.append(self.get_row_dict(row, para_text, Tag.PARA.value), ignore_index=True)
        except Exception:
            logger.error("Caught exception while Sub-heading Validation", exc_info=True)
            return dataframe
        return df

    def check_if_has_specialchar(self, text):
        break_point = 0
        for index, character in enumerate(text):
            if index > 70:
                break
            else:
                if (character in SPECIAL_CHARS) and index > 4:
                    break_point = index
        if len(text) > break_point and break_point > 5:
            return break_point
        else:
            return -1

    def get_row_dict(self, row, text, tag):
        dict_row = copy.deepcopy(row)
        dict_row['Tag'] = tag
        dict_row['Text'] = text
        return dict_row

import logging

from utils.tags import Tag
from validators.abstract_validator import AbstractValidator
from src.bullet_detector import BulletsDetector

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
ALLOWED_CONSECUTIVE_HEADINGS = 2


class Independent_Validators(AbstractValidator):
    def __init__(self):
        self.detector = BulletsDetector()
        self.tags = list()
        self.all_headings = list()
        self.all_sub_headings = list()

    def validate(self, dataframe):
        logger.debug("Running %s Validator", self.__class__.__name__)
        #bullet_map = self.detector.detect_tag_specific_bullets([Tag.HEADING.value, Tag.SUB_HEADING.value], dataframe)
        for index, row in dataframe.iterrows():
            self.layout_tag_validation(row)
            #self.bullet_type_validaton(row, bullet_map)
            #self.heading_validaton(row)
        #self.positive_check_and_update(bullet_map)
        return dataframe

    def layout_tag_validation(self, row):
        try:
            if row[Tag.PAGE_TYPE_LABEL.value] == Tag.START_PAGE.value or row[
                Tag.PAGE_TYPE_LABEL.value] == Tag.TOC_PAGE.value:
                row[Tag.TAG.value] = Tag.OTHER.value
        except Exception as ex:
            logger.error("Caught Exception while running layout_tag_validation", exc_info=True)

    def bullet_type_validaton(self, row, bullet_map):
        try:
            if Tag.HEADING.value in bullet_map.keys() and row[Tag.TAG.value] == Tag.HEADING.value:
                self.all_headings.append(row)
            if Tag.SUB_HEADING.value in bullet_map.keys() and row[Tag.TAG.value] == Tag.SUB_HEADING.value:
                self.all_sub_headings.append(row)
        except Exception as ex:
            logger.error("Caught Exception while running bullet_type_validaton", exc_info=True)

    def heading_validaton(self, row):
        try:
            if row[Tag.TAG.value] == Tag.HEADING.value:
                self.tags.append(row)
            elif len(self.tags) > ALLOWED_CONSECUTIVE_HEADINGS:
                self.convert_heads_to_paras()
                self.tags = list()
            else:
                self.tags = list()
        except Exception as ex:
            logger.error("Caught Exception while running heading_validaton", exc_info=True)

    def convert_heads_to_paras(self):
        for index in range(1, len(self.tags) - 1):
            self.tags[index][Tag.TAG.value] = Tag.PARA.value
            logger.debug("Updating row tag to PARA")
            logger.debug(self.tags[index][Tag.TEXT.value])

    def positive_check_and_update(self, bullet_map):
        if len(self.all_headings) > 0 and len(self.all_sub_headings) > 0:
            bullet_type_head = bullet_map.get(Tag.HEADING.value)
            bullet_type_sub_head = bullet_map.get(Tag.SUB_HEADING.value)
            for row in self.all_headings:
                row_text = row[Tag.TEXT.value]
                row_bullet_type = self.detector.detect_most_probable_bullet(row_text)
                logger.debug("Row_Text: %s", row_text)
                logger.debug("Bullet_Type: %s", row_bullet_type)
                if row_bullet_type == bullet_type_sub_head:
                    row[Tag.TAG.value] = Tag.SUB_HEADING.value
                    logger.debug("Validated and converted Heading to Sub-Heading")
                    logger.debug("Row Text: %s", row_text)
            for row in self.all_sub_headings:
                row_text = row[Tag.TEXT.value]
                row_bullet_type = self.detector.detect_most_probable_bullet(row_text)
                logger.debug("Row_Text: %s", row_text)
                logger.debug("Bullet_Type: %s", row_bullet_type)
                if row_bullet_type == bullet_type_head:
                    row[Tag.TAG.value] = Tag.HEADING.value
                    logger.debug("Validated and converted Sub-Heading to Heading")
                    logger.debug("Row Text: %s", row_text)

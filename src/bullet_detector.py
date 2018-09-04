import logging.config
from utils.tags import Tag
from bullet_templates.alpha_numeric_bullets import AlphaNumericBulletsIdentifier
from bullet_templates.float_numerical_bullets import FloatNumericalBulletsIdentifier
from bullet_templates.lower_alphabets import LowerAlphaBulletsIdentifier
from bullet_templates.numerical_bullets import NumericBulletsIdentifier
from bullet_templates.upper_alphabets import UpperAlphaBulletsIdentifier
from bullet_templates.lower_roman_bullets import LowerRomanBulletsIdentifier
from bullet_templates.upper_roman_bullets import UpperRomanBulletsIdentifier

logger = logging.getLogger(__name__)

BULLET_IDENTIFIER_MAP = {0: AlphaNumericBulletsIdentifier(),
                         1: FloatNumericalBulletsIdentifier(),
                         2: LowerAlphaBulletsIdentifier(),
                         3: UpperAlphaBulletsIdentifier(),
                         4: NumericBulletsIdentifier(),
                         5: LowerRomanBulletsIdentifier(),
                         6:UpperRomanBulletsIdentifier()
                         }
BULLET_CLASSES = {"AlphaNumericBulletsIdentifier": AlphaNumericBulletsIdentifier(),
                  "FloatNumericalBulletsIdentifier": FloatNumericalBulletsIdentifier(),
                  "LowerAlphaBulletsIdentifier": LowerAlphaBulletsIdentifier(),
                  "UpperAlphaBulletsIdentifier": UpperAlphaBulletsIdentifier(),
                  "NumericBulletsIdentifier": NumericBulletsIdentifier(),
                  "LowerRomanBulletsIdentifier": LowerRomanBulletsIdentifier(),
                  "UpperRomanBulletsIdentifier":UpperRomanBulletsIdentifier()
                  }


class BulletsDetector(object):
    def __init__(self):
        self.bullet_templates = list()
        self.bullet_templates.append(AlphaNumericBulletsIdentifier())
        self.bullet_templates.append(FloatNumericalBulletsIdentifier())
        self.bullet_templates.append(LowerAlphaBulletsIdentifier())
        self.bullet_templates.append(UpperAlphaBulletsIdentifier())
        self.bullet_templates.append(NumericBulletsIdentifier())
        self.bullet_templates.append(LowerRomanBulletsIdentifier())
        self.bullet_templates.append(UpperRomanBulletsIdentifier())

    def get_bullet(self, text):
        bullet = Tag.WHITESPACE.value
        bullet_type = self.detect_most_probable_bullet(text)
        if bullet_type != 'None':
            bullet_identifier_object = BULLET_CLASSES.get(bullet_type)
            bullets_found = bullet_identifier_object.find_bullets(text)
            if len(bullets_found) > 0:
                bullet = bullets_found[0]
        return bullet

    def detect_most_probable_bullet(self, text):
        found_template = 'None'
        for template in self.bullet_templates:
            if template.is_bullet_present(text.strip()):
                found_template = template.getName()
                break
        return found_template

    def detect_tag_specific_bullets(self, list_of_tags, dataframe):
        bullet_counts = {'Main-heading': [0, 0, 0, 0, 0, 0,0],
                         'Sub-heading': [0, 0, 0, 0, 0, 0,0],
                         'Sub-section': [0, 0, 0, 0, 0, 0,0]
                         }
        result = dict()
        r_bullet_map = {'AlphaNumericBulletsIdentifier': 0,
                        'FloatNumericalBulletsIdentifier': 1,
                        'LowerAlphaBulletsIdentifier': 2,
                        'UpperAlphaBulletsIdentifier': 3,
                        'NumericBulletsIdentifier': 4,
                        'LowerRomanBulletsIdentifier': 5,
                        'UpperRomanBulletsIdentifier':6
                        }
        for index, row in dataframe.iterrows():
            if row['Tag'] in list_of_tags:
                bullet = self.detect_most_probable_bullet(row['Text'])
                logger.debug("Text: %s", row['Text'])
                logger.debug("Identified Bullet: %s", bullet)
                if bullet != 'None':
                    index = r_bullet_map.get(bullet)
                    bullet_counts.get(row['Tag'])[index] += 1
        for tag in list_of_tags:
            max_index = 0
            max_value = 0
            for index, count in enumerate(bullet_counts.get(tag)):
                if max_value < count:
                    max_value = count
                    max_index = index
            result[tag] = BULLET_IDENTIFIER_MAP.get(max_index)
            logger.debug("Identified Bullet for %s ", tag)
            logger.debug("Bullet is %s", result[tag].getName())
        logger.debug("Found bullet templates")
        logger.debug(result)
        return result


if __name__ == '__main__':
    text = '''(x) DEFINITATIONS'''
    tester = BulletsDetector()
    bullet = tester.detect_most_probable_bullet(text)
    print(bullet)

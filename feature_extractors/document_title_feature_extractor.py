import inspect
import os
import re

from src.bullet_detector import BulletsDetector
from utils.text_utils import remove_space


class FeatureExtractor(object):
    def __init__(self, client_name):
        self.detector = BulletsDetector()
        self.text_keywords = list()
        try:
            dictionary_path_txt = os.path.join(
                os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
                '../lookup_dictionaries/' + client_name + '_doc_titles.txt')
            with open(dictionary_path_txt, mode='r') as infile:
                for line in infile.readlines():
                    self.text_keywords.append(line.strip())
        except Exception as __ex:
            print(__ex.__cause__)
            raise ValueError("Unable to read keywords from dataframe")

    def extract_features(self, text):
        text = str(text)
        text = text.strip()
        features = {
            'all_upper': str(text.isupper()),
            'all_title': str(text.istitle()),
            'length_range': str(self.length_range(text)),
            'contains_keywords': self.contains_keywords(text)
        }
        return features

    def contains_keywords(self, text):
        answer = 0
        for keyword in self.text_keywords:
            if remove_space(keyword.lower()) in remove_space(text.lower()):
                answer = 1
                break
        return answer

    def all_alpha(self, text):
        answer = 1
        for character in text:
            if not character.isalpha():
                answer = 0
                break
        return answer

    def length_range(self, text):
        length = len(text)
        if length < 5:
            return 1
        if length < 10:
            return 2
        else:
            return 3

    def trail_special_char(self, text):
        if text[-1] in [':', '-', '~', '.']:
            return 1
        else:
            return 0

    def bullet_type(self, text):
        return str(self.detector.detect_most_probable_bullet(text))

    def bracketed_num(self, text):
        if re.search(r'^\[[0-9]+\]|\([0-9]+\)', text):
            return 1
        else:
            return 0

    def bracketed_cap_alpha(self, text):
        if re.search(r'^[A-Z]\.', text):
            return 1
        else:
            return 0

    def bracketed_cap_alpha_parentheses(self, text):
        if re.search(r'^\([A-Z]+\)', text):
            return 1
        else:
            return 0

    def bracketed_cap_alpha_square(self, text):
        if re.search(r'^\[[A-Z]+\]', text):
            return 1
        else:
            return 0

    def bracketed_lower_alpha(self, text):
        if re.search(r'^[a-h j-s](\.|\))', text):
            return 1
        else:
            return 0

    def bracketed_lower_alpha_parentheses(self, text):
        if re.search(r'^\([a-h j-s]+\)', text):
            return 1
        else:
            return 0

    def bracketed_lower_alpha_square(self, text):
        if re.search(r'^\[[a-h j-s]+\]', text):
            return 1
        else:
            return 0

    def sub_head_num(self, text):
        if re.search(r'^[0-9]+\.[0-9]+\.*\s', text):
            return 1
        else:
            return 0

    def roman_num_begin(self, text):
        if re.search(r'^\((ii?i?|i?i?vi?i?i?|i?i?xi?i?i?)\)', text):
            return 1
        else:
            return 0

    def two_level_num(self, text):
        if re.search(r'^[0-9]+\.[0-9]+(?!\.[0-9])', text):
            return 1
        else:
            return 0

    def three_level_num(self, text):
        if re.search(r'^[0-9]+\.[0-9]+\.[0-9]+(?!\.[0-9])', text):
            return 1
        else:
            return 0

    def four_level_num(self, text):
        if re.search(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+', text):
            return 1
        else:
            return 0

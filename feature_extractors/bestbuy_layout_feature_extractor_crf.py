import re

import pandas as pd

from src.bullet_detector import BulletsDetector


class FeatureExtractor(object):
    def __init__(self):
        self.detector = BulletsDetector()

    def get_features(self, text, key_prefix='', is_not_padding=True):
        text = str(text)
        text = text.strip()
        clean_text = ''
        for character in text:
            if character.isalpha() or character.isspace():
                clean_text += character
        clean_text = clean_text.strip()
        features = {key_prefix + '_all_lower': str(clean_text.islower()) if is_not_padding else -1,
                    key_prefix + '_all_upper': str(clean_text.isupper()) if is_not_padding else -1,
                    key_prefix + '_all_title': str(clean_text.istitle()) if is_not_padding else -1,
                    key_prefix + '_all_alpha': self.all_alpha(text) if is_not_padding else -1,
                    key_prefix + '_first_lower': self._first_lower(clean_text) if is_not_padding else -1,
                    key_prefix + '_first_upper': self._first_upper(clean_text) if is_not_padding else -1,
                    key_prefix + '_first_title': self._first_title(clean_text) if is_not_padding else -1,
                    key_prefix + '_length_range': str(self.length_range(text)) if is_not_padding else -1,
                    key_prefix + '_bullet_type': str(self.bullet_type(text)) if is_not_padding else -1,
                    key_prefix + '_trail_special_char': self.trail_special_char(text) if is_not_padding else -1,
                    key_prefix + '_bracketed_num': self.bracketed_num(text) if is_not_padding else -1,
                    key_prefix + '_bracketed_cap_alpha': self.bracketed_cap_alpha(text) if is_not_padding else -1,
                    key_prefix + '_bracketed_lower_alpha': self.bracketed_lower_alpha(text) if is_not_padding else -1,
                    key_prefix + '_sub_head_num': self.sub_head_num(text) if is_not_padding else -1,
                    key_prefix + '_two_level_num': self.two_level_num(text) if is_not_padding else -1,
                    key_prefix + '_three_level_num': self.three_level_num(text) if is_not_padding else -1,
                    key_prefix + '_four_level_num': self.four_level_num(text) if is_not_padding else -1,
                    key_prefix + '_table_of_content': self.table_of_content(text) if is_not_padding else -1,
                    key_prefix + '_bracketed_lower_alpha_square': self.bracketed_lower_alpha_square(
                        text) if is_not_padding else -1,
                    key_prefix + '_bracketed_lower_alpha_parentheses': self.bracketed_lower_alpha_parentheses(
                        text) if is_not_padding else -1,
                    key_prefix + '_bracketed_cap_alpha_square': self.bracketed_cap_alpha_square(
                        text) if is_not_padding else -1,
                    key_prefix + '_bracketed_cap_alpha_parentheses': self.bracketed_cap_alpha_parentheses(
                        text) if is_not_padding else -1,
                    key_prefix + '_roman_num_begin': self.roman_num_begin(text) if is_not_padding else -1,
                    key_prefix + '_one_level_num': self.one_level_num(text) if is_not_padding else -1,
                    key_prefix + '_count_caps_token': self.count_caps_token(clean_text) if is_not_padding else -1,
                    key_prefix + '_mixed_caps_and_non_caps': self.mixed_caps_and_non_caps(
                        clean_text) if is_not_padding else -1,
                    key_prefix + '_mixed_title_and_non_title': self.mixed_title_and_non_title(
                        clean_text) if is_not_padding else -1,
                    key_prefix + '_ends_with_comma_period': self.ends_with_comma_period(text) if is_not_padding else -1,
                    key_prefix + '_last_is_digit': self.last_is_digit(text) if is_not_padding else -1,
                    key_prefix + '_first_two_chars_caps': self.first_two_chars_caps(text) if is_not_padding else -1,
                    key_prefix + '_contains_special_char_inside': self.contains_special_char_inside(text) if is_not_padding else -1
                    }
        return features

    def extract_features(self, texts, preceding_sentences=0, following_sentences=0):
        features = list()
        for index in range(0, len(texts)):
            sentence_feature = dict()
            p_index = preceding_sentences
            f_index = following_sentences
            # Preceding Sentences Features
            while p_index > 0:
                if index < p_index:
                    sentence_feature.update(self.get_features('', str(-p_index), is_not_padding=False))
                else:
                    sentence_feature.update(
                        self.get_features(texts[index - p_index], str(-p_index), is_not_padding=True))
                p_index -= 1
            # Current Sentence Features
            sentence_feature.update(self.get_features(texts[index]))
            # Following Sentences Features
            while f_index > 0:
                if index + f_index < len(texts):
                    sentence_feature.update(self.get_features(texts[index + f_index], str(f_index)))

                else:
                    sentence_feature.update(self.get_features('', str(f_index), is_not_padding=False))
                f_index -= 1
            features.append(sentence_feature)
        return features

    def all_alpha(self, text):
        answer = 1
        for character in text:
            if not character.isalpha():
                answer = 0
                break
        return answer

    def _first_lower(self, text):
        if len(text) > 0:
            return text.split()[0].islower()
        else:
            return 0

    def _first_upper(self, text):
        if len(text) > 0:
            return text.split()[0].isupper()
        else:
            return 0

    def _first_title(self, text):
        if len(text) > 0:
            return text.split()[0].istitle()
        else:
            return 0

    def table_of_content(self, text):
        if re.search(r'\.{5,}', text):
            return 1
        else:
            return 0

    def length_range(self, text):
        length = len(text.split(' '))
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

    def one_level_num(self, text):
        if re.search(r'^[0-9]+\s?(?!\.[0-9])', text):
            return 1
        else:
            return 0

    def two_level_num(self, text):
        if re.search(r'^[0-9]+\s?\.\s?[0-9]+(?!((\.|,)[0-9]))', text):
            return 1
        else:
            return 0

    def three_level_num(self, text):
        if re.search(r'^[0-9]+\s?\.\s?[0-9]+\s?\.\s?[0-9]+(?!\.[0-9])', text):
            return 1
        else:
            return 0

    def four_level_num(self, text):
        if re.search(r'^[0-9]+\s?\.\s?[0-9]+\s?\.\s?[0-9]+\s?\.\s?[0-9]+', text):
            return 1
        else:
            return 0

    def count_caps_token(self, clean_text):
        tokens = clean_text.split(' ')
        count = 0
        for token in tokens:
            if token.isupper():
                count += 1
        if count > 6:
            return 1
        else:
            return 0

    def mixed_caps_and_non_caps(self, clean_text):
        tokens = clean_text.split(' ')
        caps_status = False
        non_caps_status = False
        for token in tokens:
            if token.isupper() and not caps_status:
                caps_status = True
            if token.islower() and not non_caps_status:
                non_caps_status = True
        if caps_status and non_caps_status:
            return 1
        else:
            return 0

    def mixed_title_and_non_title(self, clean_text):
        tokens = clean_text.split(' ')
        title_status = False
        non_title_status = False
        for token in tokens:
            if token.istitle() and not title_status:
                title_status = True
            if not token.istitle() and not non_title_status:
                non_title_status = True
        if title_status and non_title_status:
            return 1
        else:
            return 0

    def ends_with_comma_period(self, text):
        if text[-1] in [',', '.','_','~']:
            return 1
        else:
            return 0

    def last_is_digit(self, text):
        if text[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            return 1
        else:
            return 0

    def first_two_chars_caps(self, text):
        result = 1
        if len(text) > 2:
            if text[0].isupper() and text[1].isupper():
                result = 1
            else:
                result = 0
        return result

    def contains_special_char_inside(self,text):
        threshold_position=4
        result=False
        special_chars=['(',')',',',';','~',':','/','_']
        for index in range(0, len(text)):
            char_at_index=text[index]
            if index>threshold_position and char_at_index in special_chars:
                result=True
        return result


if __name__ == '__main__':
    text = "(I)NG AND WAGES ANDOR"
    #file_path = '../datasets/erm_trainset/Assa_Abloy_-_MSA.pdf.html_3_.xlsx'
    #file_df = pd.read_excel(open(file_path, mode='rb'), sheetname='Sheet1')
    x = FeatureExtractor()
    #x.extract_features(dataframe=file_df, preceding_sentences=1, following_sentences=1)
    # print(x.get_features(text,str(-3),is_not_padding=True))
    #print(x.extract_features(dataframe=file_df,preceding_sentences=1,following_sentences=1))
    print(x.contains_special_char_inside(text))
    #print(x._first_title(text))
    #print(x._first_upper(text))
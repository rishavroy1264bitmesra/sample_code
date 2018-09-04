import re


class FooterFeatureExtractor(object):
    def __init__(self):
        self.start_pattern = re.compile(r'^\d')
        self.end_pattern = re.compile(r'\d$')
        self.contains_keyword = re.compile(r'table|table of contents|contents')
        self.periods = re.compile(r'\.{5,}')

    def get_sentences(self, dataframe):
        sentences = list()
        for index, row in dataframe.iterrows():
            sentences.append(str(row['Text']))
        return sentences

    def convert_to_text(self, dataframe):
        text = ' '
        for index, row in dataframe.iterrows():
            text = text + " " + (str(row['Text']))
        return text

    def extract_features(self, dataframe):
        sentences = self.get_sentences(dataframe)
        features = {'upper_more_than_lower': self.upper_more_than_lower(sentences),
                    'sentences_ends_with_number': self.sentences_ends_with_number(sentences),
                    'table_of_content_keywords': self.table_of_content_keywords(sentences),
                    'sentences_starts_with_number': self.sentences_starts_with_number(sentences),
                    'contains_short_sentences': self.contains_short_sentences(sentences),
                    'no_of_sentence': self.no_of_sentence(sentences),
                    'all_sentences_title': self.all_sentences_title(sentences),
                    'contains_periods': self.contains_periods(sentences)
                    }
        return features

    def no_of_sentence(self, sentences):
        length = len(sentences)
        if length < 10:
            return 1
        elif length < 25:
            return 2
        else:
            return 3

    def upper_more_than_lower(self, sentences):
        text = ' '.join(sentences)
        uppers = 0
        lowers = 0
        for character in text:
            if character.isupper():
                uppers += 1
            if character.islower():
                lowers += 1
        return uppers > lowers

    def sentences_starts_with_number(self, sentences):
        trigger_count = 0
        for sentence in sentences:
            text = sentence.strip()
            if self.start_pattern.search(text): trigger_count += 1
        if trigger_count > 3:
            return 1
        else:
            return 0

    def all_sentences_title(self, sentences):
        result = True
        for sentence in sentences:
            first_character = ''
            for character in sentence.strip():
                if character.isalpha():
                    first_character = character
                    break
        result = result and first_character.isupper()
        return result

    def sentences_ends_with_number(self, sentences):
        trigger_count = 0
        for sentence in sentences:
            text = sentence.strip()
            if self.end_pattern.search(text): trigger_count += 1
        if trigger_count > 3:
            return 1
        else:
            return 0

    def no_of_tokens(self, sentences):
        text = ' '.join(sentences)
        text = text.strip()
        tokens = text.split(' ')
        no_of_tokens = len(tokens)
        if no_of_tokens < 50:
            return 1
        elif no_of_tokens < 300:
            return 2
        else:
            return 3

    def table_of_content_keywords(self, sentences):
        result = 0
        for sentence in sentences:
            text = sentence.strip().lower()
            if self.contains_keyword.search(text): result = 1
        return result

    def contains_short_sentences(self, sentences):
        range = 50
        result = 0
        first_length = len(sentences[0])
        for sentence in sentences:
            if abs(first_length - len(sentence)) > range:
                result = 1
        return result

    def contains_periods(self, sentences):
        trigger_count = 0
        for sentence in sentences:
            text = sentence.strip()
            if self.periods.search(text): trigger_count += 1
        if trigger_count > 3:
            return 1
        else:
            return 0


if __name__ == '__main__':
    tester = FeatureExtractor()
    sentences = ['  1.2WIPRO LTD1.2', '2and1.2', '3Samsung Technologies1.2', '4.5WIPRO LTD']
    print(tester.contains_short_sentences(sentences))

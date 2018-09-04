import re

import pandas as pd

from src.bullet_detector import BulletsDetector


class Validator(object):
    def __init__(self):
        self.bullet_identifier = BulletsDetector()

    def validate(self, dataframes):
        result = list()
        for dataframe in dataframes:
            result.append(self.validate_bullet_and_split(dataframe))
        return result

    def validate_bullet_and_split(self, dataframe):
        bullets_to_validate = ['Sub-heading']
        df = pd.DataFrame(columns=dataframe.columns)
        bullets_found = self.bullet_identifier.detect_tag_specific_bullets(bullets_to_validate, dataframe)
        identifier = bullets_found.get('Sub-heading')
        new_index = -1
        for index, row in dataframe.iterrows():
            if row['Tag'] == 'Sub-heading' and identifier.is_bullet_present(row['Text']):
                splitted_text = re.split(r'(?<=\w\.)\s', row['Text'])
                sub_heading = splitted_text[0]
                para = splitted_text[1]
                new_index += 1
                df.loc[new_index] = [sub_heading, 'Sub-heading', row['Typography'], row['Top_left'],
                                     row['Bottom_right'], row['File_Name'], row['Page_style'], row['Page_Number'],
                                     row['Tag_no'], row['Document_type']]
                new_index += 1
                df.loc[new_index] = [para, 'para', row['Typography'], row['Top_left'],
                                     row['Bottom_right'], row['File_Name'], row['Page_style'], row['Page_Number'],
                                     row['Tag_no'], row['Document_type']]
            new_index += 1
            df.loc[new_index] = [row['Text'], row['Tag'], row['Typography'], row['Top_left'],
                                 row['Bottom_right'], row['File_Name'], row['Page_style'], row['Page_Number'],
                                 row['Tag_no'], row['Document_type']]
        return df

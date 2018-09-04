import json
import logging
from collections import OrderedDict

from response_generators.abstract_json_generator import AbstractJSONGenerator
from utils.tags import Tag

logger = logging.getLogger(__name__)


class FlatJSONGenerator(AbstractJSONGenerator):
    def __init__(self):
        self.paragraphs = OrderedDict()
        self.paragraphs[Tag.PARAGRAGHS_JSON_KEY.value] = list()

    def getJSON_using_dataframes(self, dataframes):
        for dataframe in dataframes:
            output = self.generate_json(dataframe)
            self.paragraphs.setdefault(Tag.PARAGRAGHS_JSON_KEY.value, []).extend(output)
        return json.dumps(self.paragraphs, indent=4)

    def generate_json(self, df):
        output = list()
        for index, row in df.iterrows():
            output.append(
                self.get_clause(row['Text'], row['Tag'], row['Bottom_right'], row['Top_left'], row['Page_style'],
                                row['Page_Number'], row['File_Name'], row['Document_type'], row['Tag_no'])
            )
        return output

    def get_clause(self, text, label, bottom_right, top_left, page_style, page_no, file_name,
                   document_type, para_id):
        return {'Text': text,
                'Label': label,
                'Bottom_Right': bottom_right,
                'File_Name': file_name,
                'Top_Left': top_left,
                'Page_Style': page_style,
                'Tag_No': str(para_id),
                'Page_Number': str(page_no),
                'Document_Type': document_type
                }

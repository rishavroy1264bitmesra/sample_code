import logging

from response_generators.abstract_json_generator import AbstractJSONGenerator
from utils.tags import Tag

logger = logging.getLogger(__name__)


class OthersResponseJSONGenerator(AbstractJSONGenerator):
    def getJSON_using_dataframes(self, dataframes):
        paragraphs = list()
        for dataframe in dataframes:
            output = self.generate_json(dataframe)
            paragraphs.extend(output)
        return paragraphs
        # return json.dumps(self.paragraphs, indent=4)

    def generate_json(self, df):
        output = list()
        for index, row in df.iterrows():
            if row['Tag'] == Tag.OTHER.value:
                output.append(
                    self.get_clause(row['Text'], row['Bottom_right'], row['Top_left'], row['Page_style'],
                                    row['Page_Number'],
                                    row['File_Name'], row['Document_type'], row['Tag_no'], row['Priority'],
                                    row[Tag.PAGE_TYPE_LABEL.value]))
        return output

    def get_clause(self, buffer, bottom_right, top_left, page_style, page_no, file_name,
                   document_type, para_id, priority, page_type):
        return {'Covered_Text': buffer,
                'Bottom_Right': str(bottom_right),
                'File_Name': file_name,
                'Top_Left': str(top_left),
                'Page_Style': page_style,
                'Tag_No': str(para_id),
                'Page_Number': str(page_no),
                'Document_Type': document_type,
                'Page_Type': page_type,
                'Priority': priority
                }

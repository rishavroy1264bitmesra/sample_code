import logging

from response_generators.abstract_json_generator import AbstractJSONGenerator
from utils.tags import Tag

logger = logging.getLogger(__name__)


class TOCPageJSONGenerator(AbstractJSONGenerator):
    def getJSON_using_dataframes(self, dataframes):
        paragraphs = list()
        for dataframe in dataframes:
            output = self.generate_json(dataframe)
            paragraphs.extend(output)
        return paragraphs
        # return json.dumps(self.paragraphs, indent=4)

    def generate_json(self, df):
        output = list()
        heading = ''
        top_left = list()
        bottom_right = list()
        para_id = list()
        page_style = ''
        page_no = list()
        sub_heading = ''
        buffer = ''
        file_name = ''
        document_type = ''
        priority = ''
        to_add = False
        for index, row in df.iterrows():
            if row[Tag.PAGE_TYPE_LABEL.value] == Tag.TOC_PAGE.value:
                buffer += ' ' + row['Text']
                top_left.append(row['Top_left'])
                bottom_right.append(row['Bottom_right'])
                para_id.append(row['Tag_no'])
                page_no.append(row['Page_Number'])
                page_style = row['Page_style']
                file_name = row['File_Name']
                document_type = row['Document_type']
                priority = row['Priority']
                to_add = True

        if to_add:
            output.append(
                self.get_clause(heading, sub_heading, buffer, bottom_right[-1], top_left[0], page_style, page_no,
                                file_name, document_type, para_id, priority))
        return output

    def get_clause(self, heading, sub_heading, buffer, bottom_right, top_left, page_style, page_no, file_name,
                   document_type, para_id, priority):
        return {'Clause': {'Main-heading': heading, 'Sub-heading': sub_heading, 'Sub-section': buffer},
                'Bottom_Right': str(bottom_right),
                'File_Name': file_name,
                'Top_Left': str(top_left),
                'Page_Style': page_style,
                'Tag_No': str(para_id),
                'Page_Number': str(page_no),
                'Document_Type': document_type
            , 'Priority': priority
                }

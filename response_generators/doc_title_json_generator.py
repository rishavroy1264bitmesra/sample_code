import logging

from response_generators.abstract_json_generator import AbstractJSONGenerator
from utils.tags import Tag

logger = logging.getLogger(__name__)


class DocTitleResponseJSONGenerator(AbstractJSONGenerator):
    def getJSON_using_dataframes(self, dataframes):
        paragraphs = list()
        for dataframe in dataframes:
            output = self.generate_json(dataframe)
            paragraphs.extend(output)
        return paragraphs
        # return json.dumps(self.paragraphs, indent=4)

    def generate_json(self, df):
        output = list()
        file_name = ''
        priority = ''
        doc_type = ''
        for index, row in df.iterrows():
            file_name = row['File_Name']
            doc_type = row['Document_type']
            priority = row['Priority']
            if row[Tag.DOCUMENT_TITLE_LABEL.value] == Tag.FOUND_TITLE.value:
                output.append(
                    self.get_clause(row['Text'], row['Page_Number'], file_name, doc_type,
                                    row['Tag_no'], priority))
        if len(output) == 0:
            output.append(
                self.get_clause("", "", file_name, doc_type,
                                "", priority))
        return output

    def get_clause(self, buffer, page_no, file_name, document_type, para_id, priority):
        return {
            'attribute_name': 'Document Title',
            'file_name': file_name,
            'line_id': [str(para_id)],
            'page_number': [str(page_no)],
            'document_type': document_type,
            'priority': priority,
            'attribute_value': buffer
        }

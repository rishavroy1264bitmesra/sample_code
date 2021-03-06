__author__ = 'Rishav'
import copy
from collections import deque, OrderedDict

from objects.paragraph import Paragraph
from objects.row_content import RowContent
from response_generators.abstract_json_generator import AbstractJSONGenerator
from src.bullet_detector import BulletsDetector
from utils.generator_utils import GeneratorUtils
from utils.tags import Tag


class LineIdsDictResponseJSONGenerator(AbstractJSONGenerator):
    '''Class responsible for generation of JSON Response for Paragraphs, Not Logging anything, if bug comes Please debug using pycharm debugger.'''

    def __init__(self):
        self.util = GeneratorUtils()
        self.bullet_detector = BulletsDetector()

    def getJSON_using_dataframes(self, dataframes):
        paragraphs = list()
        for dataframe in dataframes:
            output = self.generate_json(dataframe)
            paragraphs.extend(output)
        return paragraphs

    def generate_json(self, df):
        output = list()
        paraQueue = deque()
        headerStack = list()
        subHeaderStack = list()
        for index, row in df.iterrows():
            content = RowContent(row)
            if content.tag == Tag.HEADING.value:
                if len(headerStack) != 0 or len(subHeaderStack) != 0 or len(paraQueue) != 0:
                    output.append(self.__addHeadingClause(headerStack, subHeaderStack, paraQueue))
                headerStack.append(content)
            if content.tag == Tag.SUB_HEADING.value:
                if len(subHeaderStack) != 0 or len(paraQueue) != 0:
                    output.append(self.__addSubHeadingClause(headerStack, subHeaderStack, paraQueue))
                subHeaderStack.append(content)
            if content.tag in [Tag.PARA.value, Tag.SUB_SECTION.value]:
                paraQueue.append(content)
        if len(headerStack) != 0 or len(subHeaderStack) != 0 or len(paraQueue) != 0:
            output.append(self._addRemainingClause(headerStack, subHeaderStack, paraQueue))
        return output

    def __addSubHeadingClause(self, headerStack, subHeaderStack, paraQueue):
        # pop para # pop subheading # peek head # add clause
        dummyRowContent = self._getDummyRowContent(headerStack, subHeaderStack, paraQueue)
        subheading = self._get_subheading(subHeaderStack, dummyRowContent)
        para = self._get_all_paras(paraQueue, dummyRowContent)
        heading = self._get_heading(headerStack, dummyRowContent, False)
        return self._get_clause(heading, subheading, para)

    def __addHeadingClause(self, headerStack, subHeaderStack, paraQueue):
        # pop para # pop subheading # pop head # add clause
        dummyRowContent = self._getDummyRowContent(headerStack, subHeaderStack, paraQueue)
        subheading = self._get_subheading(subHeaderStack, dummyRowContent)
        para = self._get_all_paras(paraQueue, dummyRowContent)
        heading = self._get_heading(headerStack, dummyRowContent, True)
        return self._get_clause(heading, subheading, para)

    def _addRemainingClause(self, headerStack, subHeaderStack, paraQueue):
        # pop para # pop subheading # peek head # add clause
        dummyRowContent = self._getDummyRowContent(headerStack, subHeaderStack, paraQueue)
        subheading = self._get_subheading(subHeaderStack, dummyRowContent)
        para = self._get_all_paras(paraQueue, dummyRowContent)
        heading = self._get_heading(headerStack, dummyRowContent, False)
        return self._get_clause(heading, subheading, para)

    def _get_all_paras(self, paraQueue, dummyRowContent):
        if len(paraQueue) == 0:
            para = copy.deepcopy(dummyRowContent)
            para.tag = Tag.PARA.value
        else:
            para = paraQueue.popleft()
            while (len(paraQueue) > 0): para.merge_subsections_and_lineids_for_dict_response(paraQueue.popleft())
        return para

    def _get_subheading(self, subHeaderStack, dummyRowContent):
        if len(subHeaderStack) == 0:
            subheading = copy.deepcopy(dummyRowContent)
            subheading.tag = Tag.SUB_HEADING.value
        else:
            subheading = subHeaderStack.pop()
        return subheading

    def _get_heading(self, headerStack, dummyRowContent, pop_head):
        if len(headerStack) == 0:
            heading = copy.deepcopy(dummyRowContent)
            heading.tag = Tag.HEADING.value
        elif pop_head:
            heading = headerStack.pop()
        else:
            heading = headerStack[0]
        return heading

    def _getDummyRowContent(self, headerStack, subHeaderStack, paraQueue):
        row = self._getDummyRow(headerStack, subHeaderStack, paraQueue)
        dummyRowContent = copy.deepcopy(row)
        dummyRowContent.buffer = Tag.WHITESPACE.value
        return dummyRowContent

    def _getDummyRow(self, headerStack, subHeaderStack, paraQueue):
        para_length = len(paraQueue)
        sub_header_length = len(subHeaderStack)
        header_length = len(headerStack)
        if para_length > 0:
            row = paraQueue[0]
        elif sub_header_length > 0:
            row = subHeaderStack[0]
        elif header_length > 0:
            row = headerStack[0]
        else:
            raise ValueError("All Headers, SubHeader, Para are empty, cannot return dummy row.")
        return row

    # Uncomment the code below to get word level styles
    def _get_clause(self, heading, subheading, para):
        clause = OrderedDict()
        # sub_section_word_styles = self.split_words_styles(para.words_styles)
        clause['Main-heading'] = {heading.para_id[0]: heading.buffer}
        clause['Main_heading_No'] = self.bullet_detector.get_bullet(heading.buffer)
        clause['Sub-heading'] = {subheading.para_id[0]: subheading.buffer}
        clause['Sub_heading_No'] = self.bullet_detector.get_bullet(subheading.buffer)
        clause['Sub-section'] = self.split_para(para)
        # clause['Words-metadata'] = WordsStyles(self.get_style(heading.buffer, heading.words_styles),
        #                                       self.get_style(subheading.buffer, subheading.words_styles),
        #                                      self.get_style(para.buffer, sub_section_word_styles)).__dict__
        para_id = list()
        page_no = self.util.sort(para.page_no)
        para_id.extend(subheading.para_id)
        para_id.extend(para.para_id)
        para_id = self.util.sort(para_id)
        paragraph = Paragraph(
            clause,
            para.bottom_right,
            subheading.top_left, heading.page_style, para_id, page_no, heading.file_name,
            heading.document_type,
            heading.priority)
        return paragraph.__dict__

    def split_para(self, para):
        result = list()
        lineids = list()
        sub_sections_lineids = list()
        sub_sections_texts_array = para.buffer.split(Tag.SUB_SECTION_SPLITTER.value)
        for element in para.para_id:
            if element == Tag.SUB_SECTION_SPLITTER.value:
                sub_sections_lineids.append(lineids)
                lineids = list()
            else:
                lineids.append(element)
        sub_sections_lineids.append(lineids)
        # updates the ids in para to continue generation of Tag_No in final response
        self.update_paraids(para, sub_sections_lineids)
        if len(sub_sections_texts_array) == len(sub_sections_lineids):
            for index in range(0, len(sub_sections_texts_array)):
                lines_text_array = sub_sections_texts_array[index].split(Tag.PARA_ARRAY_SPLITTER.value)
                lineids_array = sub_sections_lineids[index]
                if len(lineids_array) == len(lines_text_array):
                    response_dict = OrderedDict()
                    for iterator in range(0, len(lineids_array)):
                        line_id = lineids_array[iterator]
                        text = lines_text_array[iterator].strip()
                        if len(text) > 0:
                            response_dict[line_id] = text
                    if any(response_dict):
                        result.append(response_dict)
                else:
                    print(lineids_array)
                    print(lines_text_array)
                    raise ValueError("Mismatch in number line texts and line ids")
        else:
            raise ValueError("Mismatch in number of para text and lineids")
        return result

    def update_paraids(self, para, sub_sections_lineids):
        para_id = list()
        for lineids in sub_sections_lineids:
            para_id.extend(lineids)
        para.para_id = para_id

    def get_style(self, text, words_styles):
        if text == Tag.WHITESPACE.value:
            return []
        else:
            return words_styles

    def split_words_styles(self, sub_section_word_styles):
        sub_sections = list()
        style = list()
        for element in sub_section_word_styles:
            if element == Tag.SUB_SECTION_SPLITTER.value:
                sub_sections.append(style)
                style = list()
            else:
                style.append(element)
        sub_sections.append(style)
        return sub_sections

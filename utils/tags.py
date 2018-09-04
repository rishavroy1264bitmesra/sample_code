from enum import Enum


class Tag(Enum):
    HTML_H1 = 'h1'
    HTML_H2 = 'h2'
    HTML_H3 = 'h3'
    GENERIC = 'generic'
    ISDA = 'isda'
    BESTBUY = 'bestbuy'
    WHITESPACE = ' '
    HEADING = 'Main-heading'
    SUB_HEADING = 'Sub-heading'
    SUB_SECTION = 'Sub-section'
    PARA = 'para'
    OTHER = 'other'
    PARAGRAGHS_JSON_KEY = 'Paragraphs'
    PAGE_NUMBER = 'Page_Number'
    START_PAGE_JSON_KEY = 'Start'
    TOC_JSON_KEY = 'Table_of_Contents'
    CLAUSE_KEY = 'Clause'
    COMMA = ','
    CLUSTER_LABEL = 'Cluster_Label'
    TOC_PAGE = 'TOC_Page'
    CONTENT_PAGE = 'Content_Page'
    START_PAGE = 'Start_Page'
    PAGE_TYPE_LABEL = 'Page_Type_Label'
    DOCUMENT_TITLE_LABEL = 'Document_Title'
    DOCUMENT_TITLE_JSON_KEY = 'Document_Titles'
    DOCUMENT_TITLE_ID = 'Document_Title_Id'
    TAG = 'Tag'
    TEXT = 'Text'
    SUB_SECTION_SPLITTER = '##@@@##'
    PARA_ARRAY_SPLITTER = '&&@@@&&'
    FOUND_TITLE = 'Found_Title'
    NOT_FOUND = 'Not_Found'
    ERM = 'erm'
    T_MOBILE = 't_mobile'
    CLIENT_NAME = 'Client'
    DOCTITLES_KEYWORDS = 'DOCTITLES_KEYWORDS'
    ATTRIBUTE_NAME = 'attribute_name'
    ATTRIBUTE_VALUE = 'attribute_value'
    ROOT_LOGGER = 'root'
    LINE_IDS_MAP = 'Line_Ids_Map'
    LINE_ID='Tag_no'


if __name__ == '__main__':
    x = [1, 2, 3]
    print(x)
    x.append("Rishav")
    print(x)

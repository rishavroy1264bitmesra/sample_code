__author__ = 'Rishav'
import logging

import pandas as pd
from objects.document import UnitDocument
logger = logging.getLogger(__name__)


class HTMLReader(object):
    def __init__(self):
        self.columns = ['Text', 'Typography', 'Top_left', 'Bottom_right', 'File_Name', 'Page_style', 'Page_Number',
                        'Tag_no', 'Document_type', 'Priority', 'Word_Style']
        self.documents_dfs = list()

    def get_doc_as_dataframes(self, dict_of_html_files, file_names):
        logger.debug("Parsing HTML files, to extract tag attributes.")
        try:
            for index, document_type in enumerate(dict_of_html_files.keys()):
                content = dict_of_html_files.get(document_type)
                soup = content
                df = self.fill_dataframe(soup, file_names[index], document_type)
                document_df = UnitDocument(html_content=content,dataframe=df)
                self.documents_dfs.append(document_df)
            logger.debug("Generated Dataframes for %s HTML files  ", len(self.documents_dfs))
        except Exception as ex:
            logger.error("Caught exception while Parsing HTML file ", exc_info=True)
        return self.documents_dfs

    def fill_dataframe(self, soup, file_name, document_type):
        df = pd.DataFrame(columns=self.columns)
        index = -1
        priority = soup['priority']
        for line_tag in soup.find_all('line'):
            text = line_tag['text'].strip()
            tag_no = line_tag['id']
            is_bold = 1
            top_left_style = []
            words_styles = []
            for html_tag in line_tag.find_all('div', {'class': 'p'}):
                is_bold = self.is_bold(html_tag, is_bold)
                word_style = str(html_tag['style'])
                word_text = html_tag.text.strip()
                page_num = html_tag.parent.parent['id']
                page_style = html_tag.parent.parent['style']
                top_left_style.append(str(html_tag['style']))
                words_styles.append((word_text, word_style))
            if len(text) > 0:
                index += 1
                df.loc[index] = [text, is_bold, self.get_top_left(style_list=top_left_style),
                                 self.get_bottom_right(style_list=top_left_style), file_name, page_style, page_num,
                                 str(tag_no),
                                 document_type[2:], priority, words_styles]
        return df

    def get_top_left(self, style_list):
        top_left = style_list[0].split(';')
        top_left = ';'.join([top_left[0], top_left[1]])
        return top_left

    def get_bottom_right(self, style_list):
        bottom_right = style_list[-1].split(';')
        bottom_right = ';'.join([bottom_right[0], bottom_right[1]])
        return bottom_right

    def is_bold(self, html_tag, is_bold):
        pass

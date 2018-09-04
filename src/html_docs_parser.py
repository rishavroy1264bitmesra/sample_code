__author__ = 'Rishav'
import logging

import pandas as pd

logger = logging.getLogger(__name__)


class HTMLReader(object):
    def __init__(self):
        self.columns = ['Text', 'Typography', 'Top_left', 'Bottom_right', 'File_Name', 'Page_style', 'Page_Number',
                        'Tag_no', 'Document_type', 'Priority']
        self.dataframes = list()

    def get_doc_as_dataframes(self, dict_of_html_files, file_names):
        for index, document_type in enumerate(dict_of_html_files.keys()):
            content = dict_of_html_files.get(document_type)
            soup = content
            df = self.fill_dataframe(soup, file_names[index], document_type)
            self.dataframes.append(df)
        logger.debug("Generated Dataframes for %s html files  ", len(self.dataframes))
        return self.dataframes

    def fill_dataframe(self, soup, file_name, document_type):
        df = pd.DataFrame(columns=self.columns)
        index = -1
        priority = soup['priority']
        for para_tag in soup.find_all('para'):
            text = para_tag['text'].strip()
            tag_no = para_tag['id']
            is_bold = 1
            top_left_style = []
            for html_tag in para_tag.find_all('div', {'class': 'p'}):
                is_bold = self.is_bold(html_tag, is_bold)
                page_num = html_tag.parent.parent['id']
                page_style = html_tag.parent.parent['style']
                top_left_style.append(str(html_tag['style']))
            if len(text) > 0:
                index += 1
                df.loc[index] = [text, is_bold, self.get_top_left(style_list=top_left_style),
                                 self.get_bottom_right(style_list=top_left_style), file_name, page_style, page_num,
                                 str(tag_no),
                                 document_type[2:], priority]
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

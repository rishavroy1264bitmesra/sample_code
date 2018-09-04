import logging
from utils.tags import Tag
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class HTMLGeneratorRunner(object):
    def __init__(self):
        self.df_to_wrap_counter = 0
        self.wrapped_tags_counter = 0

    def run_html_generators(self, dataframes, data):
        html_content = ''
        try:
            soup = BeautifulSoup(data, 'html.parser')
            htmllines, df_lines = self.get_htmllines_dflines(html_content=soup, dfs=dataframes)
            for row in df_lines:
                wrapper_tag = self.generate_wrapper_tag(soup, row)
                if wrapper_tag is not None:
                    line_id=row[Tag.LINE_ID.value]
                    htmllines[line_id].wrap(wrapper_tag)
                    self.wrapped_tags_counter += 1
            logger.info("Classified Headings(h1)/Sub-headings(h2)/Sub-sections(h3) to wrap: %s",
                        self.df_to_wrap_counter)
            logger.info("Successfully wrapped lines: %s", self.wrapped_tags_counter)
            html_content = soup.prettify('utf-8')
        except Exception as ex:
            logger.error("Caught exception while, generating normal HTML response", exc_info=True)
        return html_content

    def generate_wrapper_tag(self, content, row):
        label = row[Tag.TAG.value]
        wrapper_text = None
        wrapper_tag = None
        if label == Tag.HEADING.value:
            wrapper_text = Tag.HTML_H1.value
        elif label == Tag.SUB_HEADING.value:
            wrapper_text = Tag.HTML_H2.value
        # elif label == Tag.SUB_SECTION.value:
        #     wrapper_text = Tag.HTML_H3.value
        if wrapper_text is not None:
            self.df_to_wrap_counter += 1
            wrapper_tag = content.new_tag(wrapper_text)
        return wrapper_tag

    def get_htmllines_dflines(self, html_content, dfs):
        htmllines = dict()
        df_lines = list()
        for line_tag in html_content.find_all('line'):
            line_id = line_tag['id']
            htmllines[line_id] = line_tag
        for df in dfs:
            for index, row in df.iterrows():
                df_lines.append(row)
        return htmllines, df_lines

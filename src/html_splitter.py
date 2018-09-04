__author__ = 'Rishav'
import logging

from bs4 import BeautifulSoup, Comment
from collections import OrderedDict

logger = logging.getLogger(__name__)


class HTMLSplitter(object):
    def __init__(self):
        self.soup = None
        self.files = OrderedDict()

    def split_input_file(self, data):
        logger.debug("Splitting HTML file to multiple HTML files, based on document type.")
        file_names = []
        try:
            counter = 10
            self.soup = BeautifulSoup(data, 'html.parser')
            file_name = self.soup.find('title').text
            logger.info("Processing File: %s", file_name)
            for script in self.soup(
                    ["script", "style", "tr", "td", "table", "head"]):  # remove all javascript and stylesheet code
                script.extract()
            comments = self.soup.findAll(text=lambda text: isinstance(text, Comment))
            for comment in comments:
                comment.extract()
            scriptTags = self.soup.findAll('div')
            for script in scriptTags:
                if script.has_attr('document_type') and script.has_attr('priority'):
                    self.files[str(counter) + script['document_type'].strip()] = script
                    counter += 1
            file_names = [file_name] * len(self.files.keys())
            logger.debug("Successfully splitted into %s HTML files.", len(file_names))
        except Exception as ex:
            logger.error("Caught exception while splitting HTML file ", exc_info=True)
        return self.files, file_names

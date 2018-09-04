import inspect
import os

from src.html_splitter import HTMLSplitter

SAMPLE_FILE = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
                           '../../sanity_test.html')


class TestExecutor(object):
    def test_html_splitting(self):
        splitter = HTMLSplitter()
        with open(SAMPLE_FILE, 'r', encoding='ISO-8859-1') as f_read:
            data = f_read.read()
        files_dict, file_names = splitter.split_input_file(data)
        assert len(files_dict.keys()) == 2

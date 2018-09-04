import inspect
import os

from src.pipeline_executor import Executor
from utils.tags import Tag

SAMPLE_FILE = os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
                           '../sanity_test.html')


class TestExecutor(object):
    def test_response_generation(self):
        with open(SAMPLE_FILE, 'r', encoding='ISO-8859-1') as f_read:
            data = f_read.read()
        executor = Executor(Tag.ERM.value)
        assert executor.execute(data) != ''

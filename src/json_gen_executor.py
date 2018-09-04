import json
from collections import OrderedDict
import logging
from response_generators.others_json_generator import OthersResponseJSONGenerator
from response_generators.sub_section_json_generator import ResponseJSONGenerator
from response_generators.doc_title_json_generator import DocTitleResponseJSONGenerator
from response_generators.lineids_dict_sub_section_json_generator import LineIdsDictResponseJSONGenerator
from response_generators.append_lineids_dict import LineIdsDictionaryJSONGenerator
from utils.tags import Tag

logger = logging.getLogger(__name__)


class JSONGeneratorRunner(object):
    def run_generators(self, dataframes):
        result = OrderedDict()
        try:
            result[Tag.PARAGRAGHS_JSON_KEY.value] = ResponseJSONGenerator().getJSON_using_dataframes(dataframes)
            result[Tag.DOCUMENT_TITLE_JSON_KEY.value] = DocTitleResponseJSONGenerator().getJSON_using_dataframes(
                dataframes)
            result[Tag.OTHER.value] = OthersResponseJSONGenerator().getJSON_using_dataframes(dataframes)
            result[Tag.LINE_IDS_MAP.value] = LineIdsDictionaryJSONGenerator().getJSON_using_dataframes(dataframes)
        except Exception as ex:
            logger.error("Caught exception while, generating normal JSON response", exc_info=True)
        return json.dumps(result, indent=4)

    def run_lineids_generator(self, dataframes):
        result = OrderedDict()
        try:
            result[Tag.PARAGRAGHS_JSON_KEY.value] = LineIdsDictResponseJSONGenerator().getJSON_using_dataframes(
                dataframes)
            result[Tag.DOCUMENT_TITLE_JSON_KEY.value] = DocTitleResponseJSONGenerator().getJSON_using_dataframes(
                dataframes)
            result[Tag.OTHER.value] = OthersResponseJSONGenerator().getJSON_using_dataframes(dataframes)
        except Exception as ex:
            logger.error("Caught exception while, generating normal JSON response", exc_info=True)
        return json.dumps(result, indent=4)



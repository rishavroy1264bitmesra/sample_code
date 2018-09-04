import logging

from validators.independent_validations_validator import Independent_Validators
from validators.subheading_validator import SubHeadingValidator

logger = logging.getLogger(__name__)


class RunValidators(object):
    def __init__(self):
        '''Order of execution of validators is important'''
        self.validators = list()
        self.validators.append(Independent_Validators())
        self.validators.append(SubHeadingValidator())

    def run_validator(self, dataframe):
        try:
            for validator in self.validators:
                dataframe = validator.validate(dataframe)
        except Exception as ex:
            logger.error("Caught Exception while Validations", exc_info=True)
        return dataframe

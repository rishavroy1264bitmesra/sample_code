import logging

logger = logging.getLogger(__name__)


class Utils(object):
    @staticmethod
    def split_df_pagewise(dataframe):
        pagewise_df = list()
        start = 0
        no_of_pages = 0
        current_page = dataframe['Page_Number'][0]
        for index, row in dataframe.iterrows():
            if current_page != row['Page_Number']:
                pagewise_df.append(dataframe[start:index])
                no_of_pages += 1
                start = index
                current_page = row['Page_Number']
        pagewise_df.append(dataframe[start:])
        no_of_pages += 1
        logger.debug("Found %s different pages, splitted data pagewise.", no_of_pages)
        return pagewise_df


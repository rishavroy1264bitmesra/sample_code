from utils.tags import Tag


class RowContent(object):
    def __init__(self, row):
        self.tag = row['Tag']
        self.top_left = row['Top_left']
        self.bottom_right = row['Bottom_right']
        self.para_id = [row['Tag_no']]
        self.page_style = row['Page_style']
        self.page_no = [row['Page_Number']]
        self.buffer = row['Text']
        self.file_name = row['File_Name']
        self.priority = row['Priority']
        self.document_type = row['Document_type']
        self.words_styles = row['Word_Style']

    def merge_row(self, row_to_merge):
        if row_to_merge is not None:
            self.bottom_right = row_to_merge.bottom_right
            self.para_id.extend(row_to_merge.para_id)
            self.page_no.extend(row_to_merge.page_no)
            self.buffer = self.buffer + Tag.WHITESPACE.value + row_to_merge.buffer
        else:
            raise ValueError("row_to_merge is None")

    def merge_subsections(self, row_to_merge):
        if row_to_merge is not None:
            self.bottom_right = row_to_merge.bottom_right
            self.para_id.extend(row_to_merge.para_id)
            self.page_no.extend(row_to_merge.page_no)
            if row_to_merge.tag == Tag.SUB_SECTION.value:
                self.buffer = self.buffer + Tag.SUB_SECTION_SPLITTER.value + row_to_merge.buffer
                self.words_styles.append(Tag.SUB_SECTION_SPLITTER.value)
                self.words_styles.extend(row_to_merge.words_styles)
            else:
                self.buffer = self.buffer + Tag.WHITESPACE.value + row_to_merge.buffer
                self.words_styles.extend(row_to_merge.words_styles)
        else:
            raise ValueError("row_to_merge is None")

    def merge_subsections_and_lineids(self, row_to_merge):
        if row_to_merge is not None:
            self.bottom_right = row_to_merge.bottom_right
            #self.para_id.extend(row_to_merge.para_id)
            self.page_no.extend(row_to_merge.page_no)
            if row_to_merge.tag == Tag.SUB_SECTION.value:
                self.buffer = self.buffer + Tag.SUB_SECTION_SPLITTER.value + row_to_merge.buffer
                self.words_styles.append(Tag.SUB_SECTION_SPLITTER.value)
                self.words_styles.extend(row_to_merge.words_styles)
                self.para_id.append(Tag.SUB_SECTION_SPLITTER.value)
                self.para_id.extend(row_to_merge.para_id)
            else:
                self.buffer = self.buffer + Tag.WHITESPACE.value + row_to_merge.buffer
                self.words_styles.extend(row_to_merge.words_styles)
                self.para_id.extend(row_to_merge.para_id)
        else:
            raise ValueError("row_to_merge is None")

    def merge_subsections_and_lineids_for_dict_response(self, row_to_merge):
        if row_to_merge is not None:
            self.bottom_right = row_to_merge.bottom_right
            self.page_no.extend(row_to_merge.page_no)
            if row_to_merge.tag == Tag.SUB_SECTION.value:
                self.buffer = self.buffer + Tag.SUB_SECTION_SPLITTER.value + row_to_merge.buffer
                self.para_id.append(Tag.SUB_SECTION_SPLITTER.value)
                self.para_id.extend(row_to_merge.para_id)
            else:
                self.buffer = self.buffer + Tag.PARA_ARRAY_SPLITTER.value + row_to_merge.buffer
                #self.para_id.append(Tag.PARA_ARRAY_SPLITTER.value)
                self.para_id.extend(row_to_merge.para_id)
        else:
            raise ValueError("row_to_merge is None")

    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items()))
        object.__str__ = __str__
        return object



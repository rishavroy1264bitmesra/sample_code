class Paragraph(object):
    def __init__(self, clause, bottom_right, top_left, page_style, tag_no, page_no, file_name, document_type, priority):
        self.Clause = clause
        self.Bottom_Right = bottom_right
        self.Top_Left = top_left
        self.Page_Style = page_style
        self.Tag_No = str(tag_no)
        self.Page_Number = str(page_no)
        self.File_Name = file_name
        self.Document_Type = document_type
        self.Priority = priority

from objects.paragraph import Paragraph
from response_generators.abstract_json_generator import AbstractJSONGenerator
from response_generators.tree_generator import HierarchyTreeGenerator


class TreeJSONConvertor(AbstractJSONGenerator):
    def generate_json(self, dataframe):
        generator = HierarchyTreeGenerator()
        tree = generator.generateTree(dataframe)
        output = list()
        for element_array in tree.paths_to_leaves():
            heading = tree.get_node(element_array[1])
            if not heading.is_leaf():
                sub_heading = tree.get_node(element_array[2])
                if not sub_heading.is_leaf():
                    para = tree.get_node(element_array[3])
                    output.append(self.get_clause(heading.data, sub_heading.data, para.data))
        return output

    def getJSON_using_dataframes(self, dataframes):
        paragraphs = list()
        for dataframe in dataframes:
            output = self.generate_json(dataframe)
            paragraphs.extend(output)
        return paragraphs

    def get_clause(self, heading, sub_heading, para):
        paragraph = Paragraph({'Main-heading': heading, 'Sub-heading': sub_heading, 'Sub-section': para}, para.bottom_right, heading.top_left, heading.page_style,
                              [heading.para_id, sub_heading.para_id, para.para_id],
                              [heading.page_no, sub_heading.page_no, para.page_no], heading.file_name,
                              heading.document_type,
                              heading.priority)
        return paragraph.__dict__

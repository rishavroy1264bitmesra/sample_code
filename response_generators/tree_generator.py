import copy

import pandas as pd
from treelib import Tree

from objects.IDGenerator import TreeId
from objects.row_content import RowContent
from utils.tags import Tag


class HierarchyTreeGenerator(object):
    def buildTree(self, dataframes):
        trees = list()
        for dataframe in dataframes:
            trees.append(self.generateTree(dataframe))
        return trees

    def getDummyHeadAndSubHead(self, row):
        dummyHead = copy.deepcopy(row)
        dummyHead['Text'] = Tag.WHITESPACE.value
        dummyHead['Tag'] = Tag.HEADING.value
        dummyHeadContent = RowContent(dummyHead)
        dummySubHead = copy.deepcopy(row)
        dummySubHead['Text'] = Tag.WHITESPACE.value
        dummySubHead['Tag'] = Tag.SUB_HEADING.value
        dummySubHeadContent = RowContent(dummySubHead)
        return dummyHeadContent, dummySubHeadContent

    def getDummySubHead(self, row):
        dummySubHead = copy.deepcopy(row)
        dummySubHead['Text'] = Tag.WHITESPACE.value
        dummySubHead['Tag'] = Tag.SUB_HEADING.value
        dummySubHeadContent = RowContent(dummySubHead)
        return dummySubHeadContent

    def getDummyHead(self, row):
        dummyHead = copy.deepcopy(row)
        dummyHead['Text'] = Tag.WHITESPACE.value
        dummyHead['Tag'] = Tag.HEADING.value
        dummyHeadContent = RowContent(dummyHead)
        return dummyHeadContent

    def getDummyRoot(self):
        row = dict()
        row['Tag'] = Tag.WHITESPACE.value
        row['Top_left'] = Tag.WHITESPACE.value
        row['Bottom_right'] = Tag.WHITESPACE.value
        row['Tag_no'] = Tag.WHITESPACE.value
        row['Page_style'] = Tag.WHITESPACE.value
        row['Page_Number'] = Tag.WHITESPACE.value
        row['Text'] = Tag.WHITESPACE.value
        row['File_Name'] = Tag.WHITESPACE.value
        row['Priority'] = Tag.WHITESPACE.value
        row['Document_type'] = Tag.WHITESPACE.value
        dummyRootContent = RowContent(row=row)
        return dummyRootContent

    def generateTree(self, dataframe):
        rootId = 'document'
        tree = Tree()
        tree.create_node(rootId, rootId, data=self.getDummyRoot())
        headPresent = False
        subHeadPresent = False
        previousTag = Tag.WHITESPACE.value
        headId = TreeId(Tag.HEADING.value)
        subheadId = TreeId(Tag.SUB_HEADING.value)
        paraId = TreeId(Tag.PARA.value)
        for index, row in dataframe.iterrows():
            content = RowContent(row)
            if content.tag in [Tag.PARA.value, Tag.SUB_SECTION.value]:
                if not headPresent and not subHeadPresent:
                    headId.incrementID()
                    subheadId.incrementID()
                    paraId.incrementID()
                    dummyHeadContent, dummySubHeadContent = self.getDummyHeadAndSubHead(row)
                    tree.create_node(identifier=headId.getID(), data=dummyHeadContent, parent=rootId)
                    tree.create_node(identifier=subheadId.getID(), data=dummySubHeadContent, parent=headId.getID())
                    tree.create_node(identifier=paraId.getID(), data=content, parent=subheadId.getID())
                elif subHeadPresent:
                    paraId.incrementID()
                    tree.create_node(identifier=paraId.getID(), data=content, parent=subheadId.getID())
                elif headPresent and not subHeadPresent:
                    dummySubHeadContent = self.getDummySubHead(row)
                    subheadId.incrementID()
                    paraId.incrementID()
                    tree.create_node(identifier=subheadId.getID(), data=dummySubHeadContent, parent=headId.getID())
                    tree.create_node(identifier=paraId.getID(), data=content, parent=subheadId.getID())
            if content.tag == Tag.SUB_HEADING.value:
                subHeadPresent = True
                subheadId.incrementID()
                if not headPresent:
                    headId.incrementID()
                    dummyHeadContent = self.getDummyHead(row)
                    tree.create_node(identifier=headId.getID(), data=dummyHeadContent, parent=rootId)
                    tree.create_node(identifier=subheadId.getID(), data=content, parent=headId.getID())
                elif headPresent:
                    tree.create_node(identifier=subheadId.getID(), data=content, parent=headId.getID())
            if content.tag == Tag.HEADING.value:
                headPresent = True
                subHeadPresent = False
                headId.incrementID()
                tree.create_node(identifier=headId.getID(), data=content, parent=rootId)
        return tree


if __name__ == '__main__':
    df = pd.read_excel(open('../datasets/treetest.xlsx', mode='rb'), sheetname='Sheet1')
    g = HierarchyTreeGenerator()
    tree = g.generateTree(df)

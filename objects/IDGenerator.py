class TreeId(object):

    def __init__(self, tag):
        self.tag = tag
        self.counter = 0

    def getID(self):
        return self.tag + str(self.counter)

    def incrementID(self):
        self.counter+=1
        return self.tag + str(self.counter)
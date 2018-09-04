from collections import  deque


class GeneratorUtils(object):
    def sort(self, x):
        pointer = x[0]
        y = deque()
        y.append(pointer)
        for index in range(1, len(x)):
            if x[index] != pointer:
                y.append(x[index])
            pointer = x[index]
        return list(y)

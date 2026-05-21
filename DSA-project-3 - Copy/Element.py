from functools import total_ordering

@total_ordering
class Element:

    def __init__(self,key,data):
        self.key = key
        self.data = data

    def __eq__(self,other):
        return self.key == other.key

    def __lt__(self,other):
        return self.key < other.key

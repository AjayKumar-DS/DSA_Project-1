import sys
from DictBinTree import DictBinTree

T= DictBinTree()

for line in sys.stdin:
    T.insert(int(line))

sorted_list=T.orderedTraversal()

for num in sorted_list:
    print(num)
import sys
import PQHeap
from Element import Element
from bitIO import BitWriter

class Node:
    def __init__(self, byte, left=None, right=None):
        self.byte = byte
        self.left = left
        self.right = right

def make_frequency_table(file):
    freq = [0] * 256
    f = open(file, "rb")
    while True:
        b = f.read(1)
        if len(b) == 0:
            break
        freq[b[0]] += 1
    f.close()
    return freq


def make_tree(freq):
    pq = PQHeap.createEmptyPQ()
    for i in range(256):
        PQHeap.insert(pq, Element(freq[i], Node(i)))
    while len(pq) > 1:
        x = PQHeap.extractMin(pq)
        y = PQHeap.extractMin(pq)
        parent = Node(-1, x.data, y.data)
        PQHeap.insert(pq, Element(x.key + y.key, parent))
    return PQHeap.extractMin(pq).data


def make_codes(node, code, codes):
    if node.left is None and node.right is None:
        if code == "":
            code = "0"
        codes[node.byte] = code
        return
    make_codes(node.left, code + "0", codes)
    make_codes(node.right, code + "1", codes)


def encode(infile, outfile):
    freq = make_frequency_table(infile)
    root = make_tree(freq)
    codes = [""] * 256
    make_codes(root, "", codes)
    out = open(outfile, "wb")
    writer = BitWriter(out)
    for x in freq:
        writer.writeint32bits(x)
    f = open(infile, "rb")
    
    while True:
        b = f.read(1)
        if len(b) == 0:
            break
        for bit in codes[b[0]]:
            writer.writebit(int(bit))
    f.close()
    writer.close()

encode(sys.argv[1], sys.argv[2])
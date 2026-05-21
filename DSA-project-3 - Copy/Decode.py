import sys
import PQHeap
from Element import Element
from bitIO import BitReader

class Node:
    def __init__(self, byte, left=None, right=None):
        self.byte = byte
        self.left = left
        self.right = right


def make_tree(freq):
    pq = PQHeap.createEmptyPQ()
    for i in range(256):
        node = Node(i)
        e = Element(freq[i], node)
        PQHeap.insert(pq, e)

    while len(pq) > 1:
        x = PQHeap.extractMin(pq)
        y = PQHeap.extractMin(pq)
        parent = Node(-1, x.data, y.data)
        merged = Element(x.key + y.key, parent)
        PQHeap.insert(pq, merged)
    root = PQHeap.extractMin(pq)
    return root.data


def decode(infile, outfile):
    file = open(infile, "rb")
    reader = BitReader(file)
    freq = []

    for i in range(256):
        freq.append(reader.readint32bits())
    total_bytes = sum(freq)

    root = make_tree(freq)
    out = open(outfile, "wb")
    current = root
    written = 0

    while written < total_bytes:
        bit = reader.readbit()
        if bit == 0:
            current = current.left
        else:
            current = current.right

        if current.left is None and current.right is None:
            out.write(bytes([current.byte]))
            written += 1
            current = root
    out.close()
    reader.close()

if len(sys.argv) != 3:
    print("Usage: python Decode.py compressedfile outputfile")
else:
    decode(sys.argv[1], sys.argv[2])
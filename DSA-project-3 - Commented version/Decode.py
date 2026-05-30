import sys
import PQHeap
from Element import Element
from bitIO import BitReader

# We define the node class:

class Node:
    def __init__(self, byte, left=None, right=None):
        self.byte = byte
        self.left = left
        self.right = right

# We create an empty priority queue
# We build up the empty priority queue by 

# We create a leaf node from the given i
# Then we take the node, puts it into an element, where we let the frequency be the key of the node
# Afterwards we insert the element into the priority

# Once we have created all 256 elements, we iterate through the the priority queue, and extract each value two at a time, like how we did it in Encode.py. 

# With the two extracted values, we create a parent, also like we did in Encode.py, and then create the merged value as an element, by letting it's key be the sum of the children's key, and having parent
# be the data for the element, as the element needs the key and the data. 
# Then we insert it into the PQHeap

# Once we are done iterating, through the priority queue, we extract the final value, which would be the root, and then we return it

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

# For decoding our encoded file, we open the file in rb, because we want to read the raw bytes of the file

# Instead of writing the bits, now we need to read the bits, which we accomplish by using the BitReader from bitIO.py

# Now we define freq as an empty list, because we need to store the data that we read from the input file

# This is done to recreate the list of 256 counts that the encoder had

# Now we need to get the count of bytes in total, which we do by taking the sum of all the integers. We need to know the amount of total bytes in order to iterate through the bytes correctly

# We then make a tree of the 256 counts

# Then we open the output file as wb, because we want to write out raw bytes to the output file

# Then we define variable to be the root. current is used to mark the position in the tree we are in at the moment. We start from the root, as that is how our priority queue data type works

# Then we also define written, which is a variable that keeps count of how many times bytes we've written out, which we use when we iterate through all the bytes.

# In the iteration, we iterate through all the bytes, specifically by keeping track of written and total_bytes. This is done in order to prevent potential extra zero bits in the end to be counted, as the huffman codes
# from the supplied library is a multiple of eight

# For each bit we iterate through, if the bit is 0, we place it as a left leaf of the current node. else if the bit is 1, it get's placed to the right

# Each time, we also check if the node we are currently at doesn't have a leaf to the left or the right, in order to check if it is a byte. If that is the case, we write the current byte out to the output file.
# We then increment written by +1 and then set the new current position to be the root. The bitreader makes it so we advance through all the values one by one when we call readbit()

# Afterwards we close the outputfile and the bitreader. After this, we have completed the decoding process


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

# To run the program, we enter the name of the input file and the name we want for our output file

if len(sys.argv) != 3:
    print("The command-line arguments for this script has to be given in the form: python Decode.py compressedfile outputfile")
else:
    decode(sys.argv[1], sys.argv[2])
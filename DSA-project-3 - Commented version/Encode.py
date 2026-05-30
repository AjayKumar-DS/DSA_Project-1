import sys
import PQHeap
from Element import Element
from bitIO import BitWriter

# We define the node class:

class Node:
    def __init__(self, byte, left=None, right=None):
        self.byte = byte
        self.left = left
        self.right = right

# We create the specified frequency table. Values are supposed to go from 0 to 255, meaning we have 256 entries in the table because we count 0
# This is done by multiplying the value of 0 in an array 256, which creates an array that contains 0 256 times. 

# We open the file that is parsed into the function. We have to specify the second parameter to be "rb" as to make sure that what is returned is the raw bytes of the file. 
# Having the data as raw bytes is essential, as huffman encoding deals with bytes, instead of text

# Afterwards, we iterate through all the values of the file, by using read(). If the length of b is 0, then it must mean that there are no more values left and we can end the loop.

# However, b is non empty, then we count keep counting the number of frequences there are in total.
# Afterwards we can close the file, and then return the frequency.

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

# Next up, we need to use the output of the previous function in order to make the huffman tree, which we can accomplish with the help of the old PQHEAP code. 

# We first create an empty priority queue. Then we insert our values from the frequency table by index, 256 times, such that for each value in our frequency table, we add it as a node in the empty
# priority queue. Note that we also wrap it inside Element() as to define it as an element

# While the length of the priority queue is greater than 1 (which is the case because we can only continue by creating huffman trees when we can merge two values), we use extractMin() from PQHeap in order to
# remove and return the element with the lowest frequency, as is how Huffman Encoding works.

# This is one for x and y. x simply extracts the first value in the priority queue heap, which makes it so that the next value in line is the second value, which is extracted by y. Thus we get our two smallest values

# Afterwards we create a node that is meant to function as the parent of the two values. We specify that the byte value is -1, as to say
# that the byte we are dealing with, is not one of the 256 values from the frequency table, and because we have to parse a value

# We then insert the parent into the Queue, where the key of the parent is the sum of the two keys as to define the new parent node as the merged values

# We iterate until there aren't two value at once we can iterate through anymore

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

# The make_codes function is what makes it such that we convert our nodes into 0's or 1's
# The node paramter is the node itself that is currently being iterated, which we use later in the encode() function. code is the string of 0's and 1's. codes is the list of 256 entries
# If the node to the left and right is none, it must mean that the current node is not a single parent, but a byte. 

# We then store the given node in the string of 0's and 1's, where we use the byte value as the index.

# The path aka. the string of code is created each time we iterate through a node that isn't a single byte, which is the process of traversing the huffman tree until we hit a single byte

# When we traverse to the left, we let the byte in the string be defined as 0, while we let it be defined as 1 if we go to the right, as is how Huffman trees are commonly written as

# We then return the path once there are nore more children

def make_codes(node, code, codes):
    if node.left is None and node.right is None:
        codes[node.byte] = code
        return
    make_codes(node.left, code + "0", codes)
    make_codes(node.right, code + "1", codes)

# Afterwards we use encode() as to take a file as an input (infile), encode it and create a file containing the encoded values as an output (outfile)

# First we define a frequency table using our make_frequency_table function from earlier, with the file we want to encode
# Then we create a tree from the frequency table
# We then create a list of 256 emty strings. This is the container for all the huffman code for each byte

# We then start by creating our 0's and 1's by using the make_codes function. 

# We then open the outputfile in binary write mode, as we are not writing strings, but raw bytes to the output file, which is done by letting the second paramter of open() be "wb".

# Then we need to use BitWriter from the bitIo.py script on our output file, which provides the means to write single bits to disk, and to write integers as 32-bits

# For each value (x) in the frequency table, we write all the frequency counts to the outputfile as 32-bits

# Then we open the input file, and scan it once more as to save on memory, as is recommended in step 5 in the step-by-step guide to what the encode program should contain

# Afterwards we read the input file one byte at a time by setting read() to read(1). If the length of the byte we are iterating is 0, then it must mean that there are no more bytes left, and we can exit the loop

# For each specific byte, which we find by using the index of the byte, we look up the code string and then we write it out as a single bit after we convert ech character to an integer

# Then we close the input file and the bitwriter for the output file once we've exited the loop, which happens when we have iterated through all the values

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

# At last, we run the encode function that also uses the other functions in this script, and we let the given arguments be defined by our own command-line arguments. 
# The first argument is meant to be the name of the original file and the second argument is the name of the compressed file aka. the output file
# (Technically the first argument is the script name itself, so you could also call the sys.argv[1] and sys.argv[2] argument 2 and 3 respectively)

if len(sys.argv) != 3:
    print("The command-line arguments for this script has to be given in the form: python Encode.py nameOfOriginalFile nameOfCompressedFile")
else:
    encode(sys.argv[1], sys.argv[2])
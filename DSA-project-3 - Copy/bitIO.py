# Note: When a BitReader is instantiated, it must be given as argument
# a file object opened in binary reading mode ('rb'). When a BitWriter
# is instantiated, it must be given as argument a file object opened
# in binary writing mode ('wb').

# Code is based on http://rosettacode.org/wiki/Bitwise_IO#Python, with
# changes by Rolf Fagerberg.

# Bits are represented by ints, which in Python (3) can be thougth of
# as infinite bitstrings of the form ...000001XXXXXXXXX (positive
# ints) or ...111110XXXXXXX (negative ints) or ......0000000
# (zero). In the code below, some suffix (of length 8 or n) of the
# bitstring of an int constitutes the bits under consideration. The
# code is always passing from left to right in the bit sequences
# (i.e., both in the int suffix and in the file).

# For writing, note that when flush() is called, a full byte will be
# written to the file by right-filling the byte with 0's (because the
# accumulator is reset to 0 (= ......0000000) after each write). This
# is the intended functionality. If on the other hand flush() is not
# called after writing has finished, the last bits written (up to 7)
# may be lost.

# If a BitWriter is instantiated via a "with ... as ..." statement,
# flush() will automatically be called (via the __exit__() method).

# The method for checking for EOF while reading is by using
# readsucces() after each readbit(). Here is an example of use:
# 
#   while True:
#       x = bitstreamin.readbit()
#       if not bitstreamin.readsucces():  # End-of-file?
#           break
#       bitstreamout.writebit(x)

class BitWriter(object): # "(object)" present to be Python2/3-agnostic
    def __init__(self, f):
        self.accumulator = 0 # the int building up to a full byte to
                             # be written
        self.bcount = 0 # number of bits put in the accumulator so far
        self.output = f # the file object we are writing to (must be
                        # opened in binary mode)

    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()
 
    def __del__(self):
        try:
            self.flush()
        except ValueError:   # I/O operation on closed file.
            pass
 
    def close(self):
        self.flush()
        self.output.close()
        
    def writebit(self, bit):
        # if a full byte has accumulated, write it out to file
        # and reset accumulater to all 0's:
        if self.bcount == 8:
            self.flush()
        # add the new bit to the accumulator:
        if bit > 0:
            self.accumulator |= 1 << 7-self.bcount
        self.bcount += 1
 
    def _writebits(self, bits, n):
        while n > 0:
            self.writebit(bits & 1 << n-1)
            n -= 1
 
    def writeint32bits(self, intvalue):
        self._writebits(intvalue, 32)

    def flush(self):
        # Writes current accumulator to file, then
        # resets accumulator to all 0's.
        if self.bcount: # but only if any bits have accumulated
            self.output.write(bytearray([self.accumulator]))
            self.accumulator = 0
            self.bcount = 0
 
class BitReader(object): # "(object)" present to be Python2/3-agnostic
    def __init__(self, f):
        self.input = f # the file object we are reading from
                       # (must be opened in binary mode)
        self.accumulator = 0 # cache of the last byte read
        self.bcount = 0 # number of bits left unread in accumulator
        self.read = 0 # Was last read succesful? [EOF or not?]
 
    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        self.input.close()
        
    def readsucces(self):
        return self.read
    
    def readbit(self):
        if not self.bcount: # if bcount == 0 [no unread bits in accumulator]
            a = self.input.read(1)
            if a: # if not EOF [EOF = attempt at reading returns empty list]
                self.accumulator = ord(a) # int between 0 and 256, [note that
                                          # ord works for byte objects]
            self.bcount = 8 # number of unread bits in accumulator
            self.read = len(a) # remember number of bytes read (0 => EOF)
        # extract the (bcount-1)'th bit [the next bit] in the accumulator:
        rv = (self.accumulator & (1 << self.bcount-1)) >> self.bcount-1
        self.bcount -= 1 # move to next bit in accumulator
        return rv
 
    def _readbits(self, n):
        # Small things to note: 1) Since starting by v = 0
        # (...00000000) and using left shifts, the integer returned
        # will be of the type ...000001XXXXXXXXX, hence it always will
        # be positive. 2) There is no check for reading past the end
        # of the file. By the way readbit works, the accumulator will
        # just not be updated, hence its last contents before EOF will
        # be reused in a cyclic fashion.
        v = 0
        while n > 0:
            v = (v << 1) | self.readbit()
            n -= 1
        return v

    def readint32bits(self):
        # Small note: by 1) in comments for _readbits(), the integer
        # interpretation in Python of the returned bits is different
        # from the Java version of the library (if the leading bit is
        # 1, the 32 bits two's complement interpretation in Java gives
        # a negative integer, whereas in Python 3, the interpretation
        # is as a positive integer). This does not pose any problems,
        # as readint32bits() and writeint32bits are inverses of each
        # other also here in the Python version of the library (unless
        # reading past the end of the file, see 2) in comments for
        # _readbits()).
        return self._readbits(32)

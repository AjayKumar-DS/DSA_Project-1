def parent(i):
    return (i - 1) // 2

def left(i):
    return 2 * i + 1

def right(i):
    return 2 * i + 2

def min_heapify(A, i):
    l = left(i)
    r = right(i)

    if l < len(A) and A[l] < A[i]:
        smallest = l
    else:
        smallest = i

    if r < len(A) and A[r] < A[smallest]:
        smallest = r

    if smallest != i:
        A[i], A[smallest] = A[smallest], A[i]
        min_heapify(A, smallest)

def createEmptyPQ():
    return []

def insert(A, e):
    A.append(e)
    i = len(A) - 1
    while i > 0 and A[parent(i)] > A[i]:
        A[i], A[parent(i)] = A[parent(i)], A[i]
        i = parent(i)

def extractMin(A):
    minimum = A[0]
    A[0] = A[len(A) - 1]
    A.pop()
    min_heapify(A, 0)
    return minimum

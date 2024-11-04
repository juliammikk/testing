# Inf2-IADS Coursework 1, October 2019, revised October 2021
# Python source file: perfect_hashing.py
# Author: John Longley

# PART B: A STATE-OF-THE-ART PERFECT HASHING SCHEME
# (template file)

# Adapting a method of Belazzougui, Botelho and Dietzfelbinger (2008)


# Start with very crude 'mod' hashing.
# First, let's read a lowercase word as a base 27 integer:

def toInt(w):
    b = w.encode()  # returns byte sequencet
    t = 0
    for i in range(len(b)):
        t = t * 27 + b[i] - 96
    return t


# Simple mod hash with some scrambling.
# (We want hashes mod p,p' to be 'independent' when p != p'.)
# We shall take p prime for the outer hash, but not necessarily the inner ones.

def modHash(s, p):
    return (toInt(s) * 21436587 + 12345678912345) % p


# Classic 'bucket array' hash table:

# h is hashcode list, r is length of table (also modulo number), L is length of index values?
# w is key

def buildHashTable(L, h, r):
    table = [[] for i in range(r)]
    for w in L:
        table[h(w)].append(w)
    return table


# p is modulo number
def buildModHashTable(L, p):
    return buildHashTable(L, lambda w: modHash(w, p), p)
    # :worth trying out for small L and p


# Finding a suitable prime for the outer hash:
def isPrime(n):
    if n % 2 == 0 and n != 2:
        return False
    else:
        j = 3
        while j * j <= n:
            if n % j == 0:
                return False
            else:
                j += 2
        else:
            return True


def prevPrime(n):
    if n % 2 == 0:
        return prevPrime(n - 1)
    elif isPrime(n):
        return n
    else:
        return prevPrime(n - 2)


# For the mini-hashes, the following very simple enumeration works just fine
# (moduli needn't be prime, but we at least avoid multiples of 2 or 3)
# Results will later be further reduced modulo m (main table size).

def miniHash(m, j):
    d = j * 6 + 3000001
    return (lambda w: modHash(w, d) % m)


# standard merge function adjusted to sort by length of buckets in descending order
def merge(b, c):
    x = len(b) + len(c)
    d = [None] * x
    i = j = 0
    for k in range(0, x):
        if i == len(b):
            d[k] = c[j]
            j += 1
        elif j == len(c):
            d[k] = b[i]
            i += 1
        elif len(b[i][0]) >= len(c[j][0]):
            d[k] = b[i]
            i += 1
        else:
            d[k] = c[j]
            j += 1
    return d


def mergeSort(A, m, n):
    if n - m == 1:
        return [A[m]]
    else:
        p = (m + n) // 2
        B = mergeSort(A, m, p)
        C = mergeSort(A, p, n)
        return merge(B, C)


def mergeSortAll(a):
    return mergeSort(a, 0, len(a))


def hashCompress(L, m):
    # create list with tuples of buckets and their index in list L
    # sort this list by lengths of the buckets in the tuples
    sortedBuckets = mergeSortAll([(bucket, i) for i, bucket in enumerate(L)])

    # creates table with booleans corresponding to vacancy of elements
    table = [False] * m
    # create table of suitable "j"s
    hashValues = [int] * len(L)


    for words, position in sortedBuckets:
        # set j to zero to then increase it at each iteration of while
        # break while loop only once j value is found
        j = 0
        while True:
            # list of hashkeys with chosen j
            values = []
            # get a hashkey for every word in the bucket
            for word in words:
                value = miniHash(m, j)(word)
                # if hashkey isn't unique or the table at that index is already full
                # restart for loop with increased j
                if value in values or table[value]:
                    j += 1
                    break

                # if hashkey is valid append it to list
                values.append(value)

            # if valid hashkeys have been generated for each word
            # add j to j list and mark places as taken in table
            if len(values) == len(words):
                hashValues[position] = j
                for value in values:
                    table[value] = True
                break

    return hashValues


# Putting it all together:
# compact data structure for representing a perfect hash function

class Hasher:
    def __init__(self, keys, lam, load):
        # keys : list of keys to be hashed
        # lam  : load on outer table, i.e. average bucket size
        #        (higher lam means more compression but
        #        perfect hash function may be harder to construct)
        # load : desired load on resulting hash table, must be < 1
        # hashEnum : enumeration of hash functions used (e.g. miniHash)
        self.n = len(keys)
        self.r = prevPrime(int(self.n // lam))
        self.m = int(self.n // load)
        HT = buildModHashTable(keys, self.r)
        self.hashChoices = hashCompress(HT, self.m)
        # :results in a very small data structure with no trace of keys!

    def hash(self, key):
        i = modHash(key, self.r)
        h = miniHash(self.m, self.hashChoices[i])
        return h(key)


# We can double-check that our hash function really is perfect
# by building the corresponding ordinary hash table:

def checkPerfectHasher(keys, H):
    T = buildHashTable(keys, lambda key: H.hash(key), H.m)
    clashes = [b for b in T if len(b) >= 2]
    if len(clashes) == 0:
        print("No clashes!")
        # return T
    else:
        print("Clashes found.")
        return clashes


# FOR INTEREST ONLY:

# Calculating 'essential size' of a Hasher, given a crude compression scheme
# (compression itself not implemented):

import math


def compressedSizeOf(H, bitWidth, maxOutlierSize):
    cutoff = 2 ** bitWidth - 1
    outliers = len([j for j in H.hashChoices if j >= cutoff])
    intermedKeySize = math.ceil(math.log2(H.r))
    return (((H.r - outliers) * bitWidth) +
            (outliers * (maxOutlierSize + intermedKeySize)))


def bestCompression(H):
    maxOutlierSize = math.ceil(math.log2(max(H.hashChoices)))
    comprList = [(i, compressedSizeOf(H, i, maxOutlierSize))
                 for i in range(3, maxOutlierSize)]
    best = comprList[0]
    for i in range(1, len(comprList)):
        if comprList[i][1] < best[1]:
            best = comprList[i]
    return {'bestBitWidth': best[0],
            'totalBitSize': best[1],
            'bitsPerKey': best[1] / H.n}

# End of file

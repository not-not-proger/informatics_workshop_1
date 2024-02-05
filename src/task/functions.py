import math


def prod_non_zero_diag(x):
    """Compute product of nonzero elements from matrix diagonal.

    input:
    x -- 2-d numpy array
    output:
    product -- integer number


    Not vectorized implementation.
    """
    i, prod = 0, 1
    # print(min(len(x), len(x[0])))
    while i < min(len(x), len(x[0])):
        if x[i][i] != 0:
            prod *= x[i][i]
        i += 1
    return prod


def are_multisets_equal(x, y):
    """Return True if both vectors create equal multisets.

    input:
    x, y -- 1-d numpy arrays
    output:
    True if multisets are equal, False otherwise -- boolean

    Not vectorized implementation.
    """
    return sorted(x) == sorted(y)


def max_after_zero(x):
    """Find max element after zero in array.

    input:
    x -- 1-d numpy array
    output:
    maximum element after zero -- integer number

    Not vectorized implementation.
    """
    i, res = 1, None
    while i < len(x):
        if x[i - 1] == 0 and x[i] != 0:
            if res is None:
                res = x[i]
            else:
                res = max(res, x[i])
        i += 1
    return res


def convert_image(img, coefs):
    """Sum up image channels with weights from coefs array

    input:
    img -- 3-d numpy array (H x W x 3)
    coefs -- 1-d numpy array (length 3)
    output:
    img -- 2-d numpy array

    Not vectorized implementation.
    """
    out = [[0 for j in range(len(img))] for i in range(len(img[0]))]
    i = 0
    while i < len(img):
        j = 0
        while j < len(img[0]):
            # print(type(img[i][j]), img[i][j], type(coefs[0]), coefs[0])
            out[i][j] = img[i][j][0]*coefs[0] + img[i][j][1]*coefs[1] + img[i][j][2]*coefs[2]
            j += 1
        i += 1
    return out


def run_length_encoding(x):
    """Make run-length encoding.

    input:
    x -- 1-d numpy array
    output:
    elements, counters -- integer iterables

    Not vectorized implementation.
    """
    elements = []
    for e in x:
        if e not in elements:
            elements.append(e)

    return elements, [x.count(e) for e in elements]


def pairwise_distance(x, y):
    """Return pairwise object distance.

    input:
    x, y -- 2d numpy arrays
    output:
    distance array -- 2d numpy array

    Not vectorized implementation.
    """
    def get_dist(a, b):
        res = 0
        for i, j in zip(a, b):
            res += (i - j)**2
        return math.sqrt(res)
    
    out = [[0 for j in range(len(y))] for i in range(len(x))]
    i = 0
    while i < len(x):
        j = 0
        while j < len(y):
            out[i][j] = get_dist(x[i], y[j])
            j += 1
        i += 1
    return out
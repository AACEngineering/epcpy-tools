"""
The Integer decoding method is used for a segment that appears as a decimal integer in the URI,
and as a binary integer in the binary encoding.
"""


def encode_int(integer, bit_length=0):
    if not isinstance(integer, int) or integer < 0:
        raise AttributeError('Value must be a positive integer')

    return '{integer:0{bit_length}b}'.format(integer=integer, bit_length=bit_length)


def decode_int(integer_bin):
    return int(integer_bin, 2)

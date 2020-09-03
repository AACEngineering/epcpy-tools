"""
The Partition Table encoding method is used for a segment that appears in the URI as a pair
of variable-length numeric fields separated by a dot (“.”) character, and in the binary
encoding as a 3-bit “partition” field followed by two variable length binary integers.

The number of characters in the two URI fields always totals to a constant number of
characters, and the number of bits in the binary encoding likewise totals to a constant
number of bits. The Partition Table encoding method makes use of a “partition table.”
The specific partition table to use is specified in the coding table for a given EPC scheme.
"""

from .integer import encode_int, decode_int


def encode_partition(parition_value, c, c_length, d, d_length, c_digits=None, d_digits=None):
    """
    The input to the encoding method is the URI portion indicated in the “URI portion” row of
    the encoding table. This consists of two strings of digits separated by a dot (“.”) character.
    For the purpose of this encoding procedure, the digit strings to the left and right of the dot
    are denoted C and D, respectively.
    """
    if not isinstance(c, int):
        try:
            c = int(c)
        except ValueError:
            raise AttributeError('c must be an integer')
    if not isinstance(d, int):
        try:
            d = int(d)
        except ValueError:
            raise AttributeError('d must be an integer')

    if c.bit_length() > c_length:
        raise AttributeError('c must have a bit length less than c_length (%d)' % c_length)
    if d.bit_length() > d_length:
        raise AttributeError('d must have a bit length less than d_length (%d)' % d_length)

    # If no digits are available, set the value to 0 per the EPC standard.
    if c_digits == 0:
        c = 0
    if d_digits == 0:
        d = 0

    return '{partition:03b}{c}{d}'.format(
        partition=parition_value, c=encode_int(c, c_length), d=encode_int(d, d_length)
    )


def decode_partition(bin_string, c_length, d_length, start_pos=0):
    """
    The input to the decoding method is the bit string identified in the “bit position” row of
    the coding table. Logically, this bit string is divided into three substrings, consisting
    of a 3-bit “partition” value, followed by two substrings of variable length.
    """
    c_end = start_pos + c_length
    d_end = c_end + d_length

    c = decode_int(bin_string[start_pos:c_end])
    d = decode_int(bin_string[c_end:d_end])
    return c, d

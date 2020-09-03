"""
The String Partition Table encoding method is used for a segment that appears in the URI as
a variable-length numeric field and a variable-length string field separated by a dot
(“.”) character, and in the binary encoding as a 3-bit “partition” field followed by
a variable length binary integer and a variable length binary-encoded character string.

The number of characters in the two URI fields is always less than or equal to a known
limit (counting a 3-character escape sequence as a single character), and the number of
bits in the binary encoding is padded if necessary to a constant number of bits.

The Partition Table encoding method makes use of a “partition table.” The specific
partition table to use is specified in the coding table for a given EPC scheme.
"""

from .string import decode_string, encode_string
from .integer import encode_int, decode_int


def encode_string_partition(parition_value, c, c_length, d, d_length):
    """
    The input to the encoding method is the URI portion indicated in the “URI portion” row
    of the encoding table for each scheme. This consists of two strings separated by a dot
    (“.”) character.

    The strings to the left and right of the dot are denoted C and D, respectively.
    """
    if c.bit_length() > c_length:
        raise AttributeError('c must have a bit length less than c_length (%d)' % c_length)

    return '{partition:03b}{c}{d}'.format(
        partition=parition_value, c=encode_int(c, c_length), d=encode_string(d, d_length)
    )


def decode_string_partition(bin_string, c_length, d_length, start_pos=0):
    """
    The input to the decoding method is the bit string identified in the “bit position” row of
    the coding table. This length of this bit string is always a multiple of seven.
    """
    c_end = start_pos + c_length
    d_end = c_end + d_length

    c = decode_int(bin_string[start_pos:c_end])
    d = decode_string(bin_string[c_end:d_end])
    return c, d

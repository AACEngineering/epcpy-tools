"""
The String encoding method is used for a segment that appears as an alphanumeric string
in the URI, and as an ISO 646 (ASCII) encoded bit string in the binary encoding.
"""

_character_map = {
    # Symbol: (Hex Value, URI Form)
    '!': (0x21, '!'), '"': (0x22, '%22'), '%': (0x25, '%25'), '&': (0x26, '%26'),
    '\'': (0x27, '\''), '(': (0x28, '('), ')': (0x29, ')'), '*': (0x2a, '*'),
    '+': (0x2b, '+'), ',': (0x2c, ','), '-': (0x2d, '-'), '.': (0x2e, '.'),
    '/': (0x2f, '%2F'), '0': (0x30, '0'), '1': (0x31, '1'), '2': (0x32, '2'),
    '3': (0x33, '3'), '4': (0x34, '4'), '5': (0x35, '5'), '6': (0x36, '6'),
    '7': (0x37, '7'), '8': (0x38, '8'), '9': (0x39, '9'), ':': (0x3a, ':'),
    ';': (0x3b, ';'), '<': (0x3c, '%3C'), '=': (0x3d, '='), '>': (0x3e, '%3E'),
    '?': (0x3f, '%3F'), 'A': (0x41, 'A'), 'B': (0x42, 'B'), 'C': (0x43, 'C'),
    'D': (0x44, 'D'), 'E': (0x45, 'E'), 'F': (0x46, 'F'), 'G': (0x47, 'G'),
    'H': (0x48, 'H'), 'I': (0x49, 'I'), 'J': (0x4a, 'J'), 'K': (0x4b, 'K'),
    'L': (0x4c, 'L'), 'M': (0x4d, 'M'), 'N': (0x4e, 'N'), 'O': (0x4f, 'O'),
    'P': (0x50, 'P'), 'Q': (0x51, 'Q'), 'R': (0x52, 'R'), 'S': (0x53, 'S'),
    'T': (0x54, 'T'), 'U': (0x55, 'U'), 'V': (0x56, 'V'), 'W': (0x57, 'W'),
    'X': (0x58, 'X'), 'Y': (0x59, 'Y'), 'Z': (0x5a, 'Z'), '_': (0x5f, '_'),
    'a': (0x61, 'a'), 'b': (0x62, 'b'), 'c': (0x63, 'c'), 'd': (0x64, 'd'),
    'e': (0x65, 'e'), 'f': (0x66, 'f'), 'g': (0x67, 'g'), 'h': (0x68, 'h'),
    'i': (0x69, 'i'), 'j': (0x6a, 'j'), 'k': (0x6b, 'k'), 'l': (0x6c, 'l'),
    'm': (0x6d, 'm'), 'n': (0x6e, 'n'), 'o': (0x6f, 'o'), 'p': (0x70, 'p'),
    'q': (0x71, 'q'), 'r': (0x72, 'r'), 's': (0x73, 's'), 't': (0x74, 't'),
    'u': (0x75, 'u'), 'v': (0x76, 'v'), 'w': (0x77, 'w'), 'x': (0x78, 'x'),
    'y': (0x79, 'y'), 'z': (0x7a, 'z'),
}

_hex_map = {
    # Symbol: (Hex Value, URI Form)
    0x21: ('!', '!'), 0x22: ('"', '%22'), 0x25: ('%', '%25'), 0x26: ('&', '%26'),
    0x27: ('\'', '\''), 0x28: ('(', '('), 0x29: (')', ')'), 0x2a: ('*', '*'),
    0x2b: ('+', '+'), 0x2c: (',', ','), 0x2d: ('-', '-'), 0x2e: ('.', '.'),
    0x2f: ('/', '%2F'), 0x30: ('0', '0'), 0x31: ('1', '1'), 0x32: ('2', '2'),
    0x33: ('3', '3'), 0x34: ('4', '4'), 0x35: ('5', '5'), 0x36: ('6', '6'),
    0x37: ('7', '7'), 0x38: ('8', '8'), 0x39: ('9', '9'), 0x3a: (':', ':'),
    0x3b: (';', ';'), 0x3c: ('<', '%3C'), 0x3d: ('=', '='), 0x3e: ('>', '%3E'),
    0x3f: ('?', '%3F'), 0x41: ('A', 'A'), 0x42: ('B', 'B'), 0x43: ('C', 'C'),
    0x44: ('D', 'D'), 0x45: ('E', 'E'), 0x46: ('F', 'F'), 0x47: ('G', 'G'),
    0x48: ('H', 'H'), 0x49: ('I', 'I'), 0x4a: ('J', 'J'), 0x4b: ('K', 'K'),
    0x4c: ('L', 'L'), 0x4d: ('M', 'M'), 0x4e: ('N', 'N'), 0x4f: ('O', 'O'),
    0x50: ('P', 'P'), 0x51: ('Q', 'Q'), 0x52: ('R', 'R'), 0x53: ('S', 'S'),
    0x54: ('T', 'T'), 0x55: ('U', 'U'), 0x56: ('V', 'V'), 0x57: ('W', 'W'),
    0x58: ('X', 'X'), 0x59: ('Y', 'Y'), 0x5a: ('Z', 'Z'), 0x5f: ('_', '_'),
    0x61: ('a', 'a'), 0x62: ('b', 'b'), 0x63: ('c', 'c'), 0x64: ('d', 'd'),
    0x65: ('e', 'e'), 0x66: ('f', 'f'), 0x67: ('g', 'g'), 0x68: ('h', 'h'),
    0x69: ('i', 'i'), 0x6a: ('j', 'j'), 0x6b: ('k', 'k'), 0x6c: ('l', 'l'),
    0x6d: ('m', 'm'), 0x6e: ('n', 'n'), 0x6f: ('o', 'o'), 0x70: ('p', 'p'),
    0x71: ('q', 'q'), 0x72: ('r', 'r'), 0x73: ('s', 's'), 0x74: ('t', 't'),
    0x75: ('u', 'u'), 0x76: ('v', 'v'), 0x77: ('w', 'w'), 0x78: ('x', 'x'),
    0x79: ('y', 'y'), 0x7a: ('z', 'z'),
}


def encode_string(string, bit_length=0):
    if not isinstance(string, str):
        string = str(string)

    encoded_string = ''

    for char in string:
        try:
            encoded_string += '{:07b}'.format(_character_map[char][0])
        except KeyError:
            raise ValueError('`%s` is not a valid character for encoding' % char)

    encoded_string = encoded_string.ljust(bit_length, '0')
    return encoded_string


def url_encode_string(string):
    if not isinstance(string, str):
        string = str(string)

    encoded_string = ''

    if not isinstance(string, str):
        string = str(string)

    for char in string:
        try:
            encoded_string += _character_map[char][1]
        except KeyError:
            raise ValueError('%s is not a valid character for encoding' % char)

    return encoded_string


def decode_string(string_bin):
    decoded_string = ''

    # Split into 7 bit chunks
    for char in [string_bin[i:i + 7] for i in range(0, len(string_bin), 7)]:
        int_char = int(char, 2)

        if int_char == 0:
            # End of string
            break

        try:
            decoded_string += _hex_map[int_char][0]
        except KeyError:
            raise ValueError('`%s` is not a valid value for decoding' % hex(int_char))

    return decoded_string


def is_encodable_string(string, raise_exception=False):
    try:
        encode_string(string)
    except ValueError as e:
        if raise_exception:
            raise e
        return False
    return True


def is_decodeable_string(string_bin, raise_exception=False):
    try:
        decode_string(string_bin)
    except ValueError as e:
        if raise_exception:
            raise e
        return False
    return True

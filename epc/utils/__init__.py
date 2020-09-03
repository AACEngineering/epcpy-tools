from epc import schemes

epc_encoding_types = {
    0x00: 'Unprogrammed',
    # range(0x01, 0x2B): 'Reserved',
    0x2C: 'gdti-96',
    0x2D: 'gsrn-96',
    0x2E: 'Reserved',
    0x2F: 'usdod-96',
    0x30: 'sgtin-96',
    0x31: 'sscc-96',
    0x32: 'sgln-96',
    0x33: 'grai-96',
    0x34: 'giai-96',
    0x35: 'gid-96',
    0x36: 'sgtin-198',
    0x37: 'grai-170',
    0x38: 'giai-202',
    0x39: 'sgln-195',
    0x3A: 'gdti-113',
    0x3B: 'adi-var',
    # range(0x3C, 0xFF): 'Reserved',
}

epc_encoding_map = {
    0x32: schemes.SGLN,
    0x33: schemes.GRAI,
    0x34: schemes.GIAI,
    0x35: schemes.GID,
    0x36: schemes.SGLN,
    0x37: schemes.GRAI,
    0x38: schemes.GIAI,
}


def get_epc_header(hex_string):
    """
    Get the numeric EPC header value for a specified hex string.
    """
    # Accept hex strings prefixed by '0x'
    if hex_string[:2] == '0x':
        hex_string = hex_string[2:]

    tag_data = int(hex_string, 16)
    tag_length = tag_data.bit_length()

    # Pad the length to multiples of 16, per the EPC Tag Data Standard
    if tag_length % 16 != 0:
        tag_length += 16 - tag_length % 16

    tag_binary = '{:0{}b}'.format(tag_data, tag_length)

    return int(tag_binary[:8], 2)


def get_epc_encoding(hex_string):
    """
    Determine the encoding used on the provided tag.

    :param epc: Hexadecimal EPC tag data
    :type epc: str

    :raises LookupError: Unable to match encoding.

    :returns: Matching EPC scheme
    :rtype: class
    """
    try:
        return epc_encoding_types[get_epc_header(hex_string)]
    except IndexError:
        raise LookupError('Unable to match encoding for %s' % hex_string)


def decode_epc(hex_string):
    """
    Attempt to decode a hex string to an EPC tag. Returns a tag object if successful.

    :param epc: Hexadecimal EPC tag data
    :type epc: str

    :raises KeyError: Unable to determine tag encoding.
    :raises LookupError: Scheme not implemented for tag.

    :returns: EPC tag object
    :rtype: object
    """
    try:
        cls = epc_encoding_map[get_epc_header(hex_string)]
    except KeyError:
        raise NotImplementedError('Unknown encoding')
    except LookupError:
        raise NotImplementedError('Scheme not implemented for %s' % get_epc_encoding(hex_string))

    return cls(epc=hex_string)

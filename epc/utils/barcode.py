from epc import schemes

barcode_encoding_map = {
    '8003': schemes.GRAI,
    '8004': schemes.GIAI,
    '0088': schemes.SGLN,
}


def get_barcode_header(barcode_string):
    return barcode_string[:4]


def decode_barcode(barcode_string, company_prefix_length):
    """
    Attempt to decode a barcode to an EPC tag. Returns a tag object if successful.

    :param barcode_string: Barcode data
    :type barcode_string: str

    :param company_prefix_length: Number of digits in the company prefix
    :type company_prefix_length: int

    :raises NotImplementedError: Unable to determine tag encoding.
    :raises NotImplementedError: Scheme not implemented for barcode.

    :returns: EPC tag object
    :rtype: object
    """
    try:
        cls = barcode_encoding_map[get_barcode_header(barcode_string)]
    except KeyError:
        raise NotImplementedError('Unknown encoding')
    except LookupError:
        raise NotImplementedError(
            'Scheme not implemented for %s' % get_barcode_header(barcode_string)
        )

    return cls(barcode=barcode_string, company_prefix_length=company_prefix_length)

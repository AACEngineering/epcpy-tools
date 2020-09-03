from epc import schemes

barcode_encoding_map = {
    '8003': schemes.GRAI,
    '8004': schemes.GIAI,
    '0088': schemes.SGLN,
}


def get_barcode_header(barcode_string):
    return barcode_string[:4]


def decode_barcode(barcode_string, company_prefix_length=None):
    try:
        cls = barcode_encoding_map[get_barcode_header(barcode_string)]
    except KeyError:
        raise NotImplementedError('Unknown encoding')
    except LookupError:
        raise NotImplementedError(
            'Scheme not implemented for %s' % get_barcode_header(barcode_string)
        )

    return cls(barcode=barcode_string, company_prefix_length=company_prefix_length)

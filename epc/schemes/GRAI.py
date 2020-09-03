from epc.encoding import (
    decode_int, encode_int, decode_partition, encode_partition,
    decode_string, encode_string, is_encodable_string, url_encode_string
)

from .base import EpcScheme

_grai_partition_table = {
    # Partition Value: (Company Prefix Length (bits),
    #                   Company Prefix Length (digits),
    #                   Asset Type Length (bits))
    0: (40, 12, 4),
    1: (37, 11, 7),
    2: (34, 10, 10),
    3: (30, 9, 14),
    4: (27, 8, 17),
    5: (24, 7, 20),
    6: (20, 6, 24),
}

_grai_prefix_table = {
    # Company Prefix Length (digits): (Partition Value,
    #                                  Asset Type Length (bits)
    #                                  Asset Type Length (digits))
    12: (0, 4, 0),
    11: (1, 7, 1),
    10: (2, 10, 2),
    9: (3, 14, 3),
    8: (4, 17, 4),
    7: (5, 20, 5),
    6: (6, 24, 6),
}


class GRAI(EpcScheme):
    """
    The Global Returnable Asset Identifier EPC scheme is used to assign a unique identity to a
    specific returnable asset, such as a reusable shipping container or a pallet skid.

    General syntax:
    urn:epc:id:grai:CompanyPrefix.AssetType.SerialNumber

    Example:
    urn:epc:id:grai:0614141.12345.400
    """
    GRAI_96 = 'grai-96'
    GRAI_170 = 'grai-170'
    ENCODINGS = (
        GRAI_96, GRAI_170
    )

    HEADER_96 = 0x33
    HEADER_170 = 0x37
    HEADER_BARCODE = '8003'
    HEADERS = (
        HEADER_96, HEADER_170
    )

    SIZE_96 = 96
    SIZE_170 = 176  # While the size is really 170, set to 176 because we need a multiple of 16.
    TAG_SIZES = (
        SIZE_96, SIZE_170
    )

    FILTER_ALL = 0
    FILTER_RESERVED_1 = 1
    FILTER_RESERVED_2 = 2
    FILTER_RESERVED_3 = 3
    FILTER_RESERVED_4 = 4
    FILTER_RESERVED_5 = 5
    FILTER_RESERVED_6 = 6
    FILTER_RESERVED_7 = 7
    FILTERS = (
        (FILTER_ALL, 'All Others'),
        (FILTER_RESERVED_1, 'Reserved'),
        (FILTER_RESERVED_2, 'Reserved'),
        (FILTER_RESERVED_3, 'Reserved'),
        (FILTER_RESERVED_4, 'Reserved'),
        (FILTER_RESERVED_5, 'Reserved'),
        (FILTER_RESERVED_6, 'Reserved'),
        (FILTER_RESERVED_7, 'Reserved'),
    )

    _tag_size = None
    _tag_filter = None

    _company_prefix = None
    _company_prefix_length = None
    _asset_type = None
    _asset_type_length = None
    _serial = None

    def __init__(self, *args, **kwargs):
        self._tag_size = self.SIZE_96
        self._tag_filter = self.FILTER_ALL
        super().__init__(*args, **kwargs)

    def __int__(self):
        self.check_fields()

        partition, type_bit_length, type_digits = _grai_prefix_table[self._company_prefix_length]
        prefix_bit_length = _grai_partition_table[partition][0]

        if self._tag_size == self.SIZE_96:
            header = self.HEADER_96
            serial = encode_int(self._serial, bit_length=38)
        elif self._tag_size == self.SIZE_170:
            header = self.HEADER_170
            serial = encode_string(self._serial, bit_length=112)

        content = encode_partition(
            partition,
            self._company_prefix, prefix_bit_length,
            self._asset_type, type_bit_length, d_digits=type_digits
        )

        return int('{header:08b}{tag_filter:03b}{content}{serial}{padding}'.format(
            header=header, tag_filter=self._tag_filter, content=content, serial=serial,
            padding=('0' * 6 if self._tag_size == self.SIZE_170 else ''),
        ), 2)

    @property
    def pure_identity_uri(self):
        self.check_fields()

        if self._asset_type_length > 0:
            asset_type = '{:0{}d}'.format(self._asset_type, self._asset_type_length)
        else:
            asset_type = ''

        if self._tag_size == self.SIZE_96:
            serial = self._serial
        elif self._tag_size == self.SIZE_170:
            serial = url_encode_string(self._serial)

        return 'urn:epc:id:grai:' \
               '{_company_prefix:0{_company_prefix_length}d}.{asset_type}.{serial}'.format(
                    asset_type=asset_type, serial=serial, **self.__dict__
                )

    @property
    def tag_uri(self):
        self.check_fields()

        if self._asset_type_length > 0:
            asset_type = '{:0{}d}'.format(self._asset_type, self._asset_type_length)
        else:
            asset_type = ''

        if self._tag_size == self.SIZE_96:
            serial = self._serial
        elif self._tag_size == self.SIZE_170:
            serial = url_encode_string(self._serial)

        return 'urn:epc:tag:{encoding}:{_tag_filter}.' \
               '{_company_prefix:0{_company_prefix_length}d}.{asset_type}.{serial}'.format(
                    encoding=self.encoding, asset_type=asset_type, serial=serial, **self.__dict__
                )

    @property
    def barcode(self):
        self.check_fields()
        if self._asset_type_length > 0:
            asset_type = '{:0{}d}'.format(self._asset_type, self._asset_type_length)
        else:
            asset_type = ''

        return '{header}0{_company_prefix:0{_company_prefix_length}d}' \
               '{asset_type}{check_digit}{_serial}'.format(
                    header=self.HEADER_BARCODE, asset_type=asset_type,
                    check_digit=self.calc_check_digit(self.values['company_prefix'], asset_type),
                    **self.__dict__
                )

    @property
    def barcode_humanized(self):
        self.check_fields()
        if self._asset_type_length > 0:
            asset_type = '{:0{}d}'.format(self._asset_type, self._asset_type_length)
        else:
            asset_type = ''

        return '({header}) 0 {_company_prefix:0{_company_prefix_length}d} ' \
               '{asset_type}{has_asset_type}{check_digit} {_serial}'.format(
                    header=self.HEADER_BARCODE, asset_type=asset_type,
                    has_asset_type=' ' if asset_type != '' else '',
                    check_digit=self.calc_check_digit(self.values['company_prefix'], asset_type),
                    **self.__dict__
                )

    @property
    def encoding(self):
        encoding = None
        if self._tag_size == self.SIZE_96:
            encoding = self.GRAI_96
        elif self._tag_size == self.SIZE_170:
            encoding = self.GRAI_170
        return encoding

    @property
    def values(self):
        return {
            'size': self._tag_size,
            'filter': self._tag_filter,
            'company_prefix': '{:0{}d}'.format(self._company_prefix, self._company_prefix_length),
            'asset_type': self._asset_type,
            'serial_number': self._serial,
        }

    def filter(self, tag_filter):
        """
        The filter value is additional control information that may be included in the EPC memory
        bank of a Gen 2 tag. The intended use of the filter value is to allow an RFID reader to
        select or deselect the tags corresponding to certain physical objects, to make it easier
        to read the desired tags in an  environment where there may be other tags present in
        the environment. For example, if the goal is to read the single tag on a pallet, and it
        is expected that there may be hundreds or thousands of item-level tags present, the
        performance of the capturing application may be improved by using the Gen 2 air interface
        to select the pallet tag and deselect the item-level tags.

        Allowed values for GRAI tags:
        0 - All Others
        1 - Reserved
        2 - Reserved
        3 - Reserved
        4 - Reserved
        5 - Reserved
        6 - Reserved
        7 - Reserved
        """
        if not (tag_filter >= 0 and tag_filter <= 7):
            raise AttributeError('Filter must be between 0 and 7 (inclusive)')

        self._tag_filter = tag_filter
        return self

    def company_prefix(self, company_prefix, company_prefix_length=None):
        """
        The GS1 Company Prefix, assigned by GS1 to a managing entity. The Company Prefix is the
        same as the GS1 Company Prefix digits within a GS1 GIAI key.

        Length corresponds to the number of digits in the company prefix.
        """
        if isinstance(company_prefix, str):
            company_prefix_length = len(company_prefix)
            company_prefix = int(company_prefix)
        elif isinstance(company_prefix, int):
            if company_prefix_length is None:
                raise AttributeError(
                    'company_prefix_length must be provided if the company prefix is an integer'
                )

        if not (company_prefix_length >= 6 and company_prefix_length <= 12):
            raise AttributeError('company_prefix_length must be between 6 and 12 (inclusive)')

        self._company_prefix = company_prefix
        self._company_prefix_length = company_prefix_length
        self._asset_type_length = _grai_prefix_table[self._company_prefix_length][2]
        return self

    def asset_type(self, asset_type):
        """
        The Asset Type, assigned by the managing entity to a particular class of asset.
        """
        if isinstance(asset_type, str):
            try:
                asset_type = int(asset_type)
            except ValueError:
                raise AttributeError('asset_type must be an integer')

        self._asset_type = asset_type
        return self

    def serial_number(self, serial_number):
        """
        The Serial Number, assigned by the managing entity to an individual object. Because an EPC
        always refers to a specific physical object rather than an asset class, the serial number is
        mandatory in the GRAI-EPC.
        """
        if isinstance(serial_number, int):
            if not (serial_number.bit_length() >= 1 and serial_number.bit_length() <= 112):
                raise AttributeError(
                    'Serial number bit length must be be between 1 and 112 (inclusive)'
                )
        elif isinstance(serial_number, str):
            if not (len(serial_number) > 0 and len(serial_number) <= 16):
                raise AttributeError(
                    'Serial number length must be be between 1 and 16 (inclusive)'
                )

            is_encodable_string(serial_number, raise_exception=True)
        else:
            raise AttributeError('Invalid type for serial_number')

        self._serial = serial_number
        return self

    def decode_epc(self, hex_string):
        """
        Decode RFID tag EPC (hex string) and populate the values in the scheme.
        """
        tag_binary = super().decode_epc(hex_string)

        # Verify header
        header = decode_int(tag_binary[0:8])
        if header not in self.HEADERS:
            raise ValueError(
                'Header `{:#04x}` does not match allowed values: ({}).'.format(
                    header, ', '.join('{:#04x}'.format(h) for h in self.HEADERS)
                )
            )

        # Read tag filter
        tag_filter = decode_int(tag_binary[8:11])
        if not any(tag_filter in f for f in self.FILTERS):
            raise ValueError('Filter `%s` does not match allowed values: %s' % (
                tag_filter, self.FILTERS
            ))
        self._tag_filter = tag_filter

        # Read partition value
        partition = decode_int(tag_binary[11:14])
        if partition not in _grai_partition_table.keys():
            raise ValueError('Partition `%s` does not match allowed values: %s' % (
                partition, _grai_partition_table.keys()
            ))

        # Read tag size, determine positions of elements
        prefix_bit_length, self._company_prefix_length, type_bit_length = \
            _grai_partition_table[partition]
        self._asset_type_length = _grai_prefix_table[self._company_prefix_length][2]

        # Decode partition elements
        self._company_prefix, self._asset_type = decode_partition(
            tag_binary, prefix_bit_length, type_bit_length, start_pos=14
        )

        # Decode serial
        serial_start = 58
        if self._tag_size == self.SIZE_96:
            serial_length = 38
            self._serial = decode_int(tag_binary[serial_start:serial_start + serial_length])
        elif self._tag_size == self.SIZE_170:
            serial_length = 112
            self._serial = decode_string(tag_binary[serial_start:serial_start + serial_length])

    def decode_barcode(self, barcode, company_prefix_length):
        """
        Decode a barcode string and populate values in the scheme.
        """
        if barcode[:4] != self.HEADER_BARCODE:
            raise ValueError(
                'Barcode header does not match expected value: %s' % self.HEADER_BARCODE
            )

        company_prefix_end = company_prefix_length + 5
        asset_type_length = _grai_prefix_table[company_prefix_length][2]
        asset_type_end = asset_type_length + company_prefix_end
        check_digit_end = asset_type_end + 1

        try:
            company_prefix = barcode[5:company_prefix_end]

            if asset_type_length > 0:
                asset_type = int(barcode[company_prefix_end:asset_type_end])
                asset_type = '{:0{}d}'.format(asset_type, asset_type_length)
            else:
                asset_type = 0

            check_digit = int(barcode[asset_type_end:check_digit_end])

            if check_digit != self.calc_check_digit(company_prefix, asset_type):
                raise AttributeError('Invalid check digit (found %s, expected %s)' % (
                    check_digit, self.calc_check_digit(company_prefix, asset_type)
                ))

            serial_number = barcode[check_digit_end:]
        except IndexError:
            raise AttributeError('Invalid barcode length, or wrong company_prefix_length specified')
        except ValueError:
            raise AttributeError('Invalid asset_type in barcode')

        try:
            serial_number = int(serial_number)
        except ValueError:
            # Serial number is a string, set the encoding to GRAI-170.
            self._tag_size = self.SIZE_170

        self.company_prefix(company_prefix, company_prefix_length)
        self.asset_type(asset_type)
        self.serial_number(serial_number)

    def calc_check_digit(self, company_prefix, asset_type):
        check_string = str(company_prefix) + str(asset_type)
        evens = []
        odds = []

        for i, char in enumerate(check_string):
            if (i + 1) % 2 == 0:
                evens.append(int(char))
            else:
                odds.append(int(char))

        return (10 - (((3 * sum(evens)) + sum(odds)) % 10)) % 10

    def check_fields(self):
        super().check_fields()
        if self._tag_size is None:
            raise AttributeError('Tag size not specified')
        if self._tag_filter is None:
            raise AttributeError('Tag filter not specified')
        if self._company_prefix is None:
            raise AttributeError('Company prefix not specified')
        if self._asset_type is None:
            raise AttributeError('Asset type not specified')
        if self._serial is None:
            raise AttributeError('Serial number not specified')

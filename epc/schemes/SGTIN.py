from epc.encoding import (
    decode_int, encode_int, decode_partition, encode_partition,
    decode_string, encode_string, is_encodable_string, url_encode_string
)

from .base import EpcScheme

_sgtin_partition_table = {
    # Partition Value: (Company Prefix Length (bits),
    #                   Company Prefix Length (digits),
    #                   Item Reference (bits))
    0: (40, 12, 4),
    1: (37, 11, 7),
    2: (34, 10, 10),
    3: (30, 9, 14),
    4: (27, 8, 17),
    5: (24, 7, 20),
    6: (20, 6, 24),
}

_sgtin_prefix_table = {
    # Company Prefix Length (digits): (Partition Value,
    #                                  Item Reference Length (bits)
    #                                  Item Reference Length (digits))
    12: (0, 4, 1),
    11: (1, 7, 2),
    10: (2, 10, 3),
    9: (3, 14, 4),
    8: (4, 17, 5),
    7: (5, 20, 6),
    6: (6, 24, 7),
}


class SGTIN(EpcScheme):
    """
    The Serialised Global Trade Item Number EPC scheme is used to assign a unique identity to an
    instance of a trade item, such as a specific instance of a product or SKU.

    General syntax:
    urn:epc:id:sgtin:CompanyPrefix.ItemRefAndIndicator.SerialNumber

    Example:
    urn:epc:id:sgtin:0614141.112345.400
    """
    SGTIN_96 = 'sgtin-96'
    SGTIN_198 = 'sgtin-198'
    ENCODINGS = (
        SGTIN_96, SGTIN_198
    )

    HEADER_96 = 0x30
    HEADER_198 = 0x36
    HEADER_BARCODE = '01'
    HEADER_BARCODE_SERIAL_NUMBER = '21'
    HEADERS = (
        HEADER_96, HEADER_198
    )

    FILTER_ALL = 0
    FILTER_POS = 1
    FILTER_FULL_CASE = 2
    FILTER_RESERVED_3 = 3
    FILTER_INNER_PACK = 4
    FILTER_RESERVED_5 = 5
    FILTER_UNIT_LOAD = 6
    FILTER_INNER_ITEM = 7
    FILTERS = (
        (FILTER_ALL, 'All Others'),
        (FILTER_POS, 'Point of Sale (POS) Trade Item'),
        (FILTER_FULL_CASE, 'Full Case for Transport'),
        (FILTER_RESERVED_3, 'Reserved'),
        (FILTER_INNER_PACK, 'Inner Pack Trade Item'),
        (FILTER_RESERVED_5, 'Reserved'),
        (FILTER_UNIT_LOAD, 'Unit Load'),
        (FILTER_INNER_ITEM, 'Unit Inside Trade Item'),
    )

    SIZE_96 = 96
    SIZE_198 = 208  # While the size is really 198, set to 208 because we need a multiple of 16.
    TAG_SIZES = (
        SIZE_96, SIZE_198
    )

    _company_prefix = None
    _company_prefix_length = None
    _item_reference = None
    _item_reference_length = None
    _serial = None

    def __init__(self, *args, **kwargs):
        self._tag_size = self.SIZE_96
        self._tag_filter = self.FILTER_ALL
        super().__init__(*args, **kwargs)

    def __int__(self):
        self.check_fields()

        partition, type_bit_length, type_digits = _sgtin_prefix_table[self._company_prefix_length]
        prefix_bit_length = _sgtin_partition_table[partition][0]

        if self._tag_size == self.SIZE_96:
            header = self.HEADER_96
            serial = encode_int(self._serial, bit_length=38)
        elif self._tag_size == self.SIZE_198:
            header = self.HEADER_198
            serial = encode_string(self._serial, bit_length=144)

        content = encode_partition(
            partition,
            self._company_prefix, prefix_bit_length,
            self._item_reference, type_bit_length, d_digits=type_digits
        )

        return int('{header:08b}{tag_filter:03b}{content}{serial}{padding}'.format(
            header=header, tag_filter=self._tag_filter, content=content, serial=serial,
            padding=('0' * 6 if self._tag_size == self.SIZE_198 else ''),
        ), 2)

    @property
    def pure_identity_uri(self):
        """
        :return: The tag's pure identity URI.
        :rtype: str
        """
        self.check_fields()

        if self._item_reference_length > 0:
            item_reference = '{:0{}d}'.format(self._item_reference, self._item_reference_length)
        else:
            item_reference = ''

        if self._tag_size == self.SIZE_96:
            serial = self._serial
        elif self._tag_size == self.SIZE_198:
            serial = url_encode_string(self._serial)

        return 'urn:epc:id:sgtin:' \
               '{_company_prefix:0{_company_prefix_length}d}.{item_reference}.{serial}'.format(
                    item_reference=item_reference, serial=serial, **self.__dict__
                )

    @property
    def tag_uri(self):
        """
        :return: The tag's URI.
        :rtype: str
        """
        self.check_fields()

        if self._item_reference_length > 0:
            item_reference = '{:0{}d}'.format(self._item_reference, self._item_reference_length)
        else:
            item_reference = ''

        if self._tag_size == self.SIZE_96:
            serial = self._serial
        elif self._tag_size == self.SIZE_198:
            serial = url_encode_string(self._serial)

        return 'urn:epc:tag:{encoding}:{_tag_filter}.' \
               '{_company_prefix:0{_company_prefix_length}d}.{item_reference}.{serial}'.format(
                    encoding=self.encoding, item_reference=item_reference, serial=serial,
                    **self.__dict__
                )

    @property
    def gtin(self):
        """
        A Global Trade Item Number (GTIN) is the 14 digit GS1 Identification Key used to identify
        products. The key comprises a GS1 Company Prefix followed by an Item Reference Number
        and a Check Digit.

        :return: The GTIN-14 representation of the tag.
        :rtype: str
        """
        self.check_fields()
        if self._item_reference_length > 0:
            item_ref = '{_item_reference:0{_item_reference_length}d}'.format(**self.__dict__)
        else:
            item_ref = ''

        indicator_digit = item_ref[:1]
        item_ref = item_ref[1:]

        return '{indicator_digit}{_company_prefix:0{_company_prefix_length}d}' \
               '{item_reference}{check_digit}'.format(
                    indicator_digit=indicator_digit, item_reference=item_ref,
                    check_digit=self.calc_check_digit(
                        indicator_digit, self.values['company_prefix'], item_ref),
                    **self.__dict__
                )

    @property
    def barcode(self):
        """
        :return: The barcode representation of the tag.
        :rtype: str
        """
        self.check_fields()

        return '{header}{gtin}{serial_header}{_serial}'.format(
                    header=self.HEADER_BARCODE, gtin=self.gtin,
                    serial_header=self.HEADER_BARCODE_SERIAL_NUMBER, **self.__dict__
                )

    @property
    def barcode_humanized(self):
        """
        :return: A human readable barcode representation of the tag.
        :rtype: str
        """
        self.check_fields()

        return '({header}) {gtin} ({serial_header}) {_serial}'.format(
                    header=self.HEADER_BARCODE, gtin=self.gtin,
                    serial_header=self.HEADER_BARCODE_SERIAL_NUMBER, **self.__dict__
                )

    @property
    def encoding(self):
        encoding = None
        if self._tag_size == self.SIZE_96:
            encoding = self.SGTIN_96
        elif self._tag_size == self.SIZE_198:
            encoding = self.SGTIN_198
        return encoding

    @property
    def values(self):
        """
        :return: Dictionary containing:

            * ``size`` (int): the tag's size in bits

            * ``filter`` (int)

            * ``company_prefix`` (str)

            * ``item_reference`` (int)

            * ``serial_number`` (int *or* str)
        """
        return {
            'size': self._tag_size,
            'filter': self._tag_filter,
            'company_prefix': '{:0{}d}'.format(self._company_prefix, self._company_prefix_length),
            'item_reference': self._item_reference,
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

        Allowed values for SGTIN tags:

        +-------+-------------------+--------------------------+
        | Value | Constant          | Description              |
        +=======+===================+==========================+
        | 0     | FILTER_ALL        | All Others               |
        +-------+-------------------+--------------------------+
        | 1     | FILTER_POS        | Point of Sale Trade Item |
        +-------+-------------------+--------------------------+
        | 2     | FILTER_FULL_CASE  | Full Case for Transport  |
        +-------+-------------------+--------------------------+
        | 3     | FILTER_RESERVED_3 | Reserved                 |
        +-------+-------------------+--------------------------+
        | 4     | FILTER_INNER_PACK | Inner Pack Trade Item    |
        +-------+-------------------+--------------------------+
        | 5     | FILTER_RESERVED_5 | Reserved                 |
        +-------+-------------------+--------------------------+
        | 6     | FILTER_UNIT_LOAD  | Unit Load                |
        +-------+-------------------+--------------------------+
        | 7     | FILTER_INNER_ITEM | Unit Inside Trade Item   |
        +-------+-------------------+--------------------------+

        :param tag_filter: The filter value, defaults to ``FILTER_ALL``.
        :type tag_filter: int

        :raises AttributeError: Filter must be between 0 and 7.

        :return: The SGTIN tag object.
        :rtype: :class:`epc.schemes.SGTIN`
        """
        if not (tag_filter >= 0 and tag_filter <= 7):
            raise AttributeError('Filter must be between 0 and 7 (inclusive)')

        self._tag_filter = tag_filter
        return self

    def company_prefix(self, company_prefix, company_prefix_length=None):
        """
        The GS1 Company Prefix, assigned by GS1 to a managing entity.

        Length corresponds to the number of digits in the company prefix.

        :param company_prefix: GS1 company prefix.
        :type company_prefix: str, int

        :param company_prefix_length: Number of digits in the company prefix.
            Required when ``company_prefix`` is an int.
        :type company_prefix_length: int, optional

        :return: The SGTIN tag object.
        :rtype: :class:`epc.schemes.SGTIN`
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
        self._item_reference_length = _sgtin_prefix_table[self._company_prefix_length][2]
        return self

    def item_reference(self, item_reference):
        """
        The Item Reference is assigned by the managing entity to a particular object class.

        The Item Reference as it appears in the EPC URI is derived from the GTIN by concatenating
        the Indicator Digit of the GTIN (or a zero pad character, if the EPC URI is derived from a
        GTIN-8, GTIN-12, or GTIN-13) and the Item Reference digits, and treating the result as a
        single numeric string.

        :param item_reference: The item reference.
        :type item_reference: int, str

        :raises ValueError: item_reference must be an integer

        :return: The SGTIN tag object.
        :rtype: :class:`epc.schemes.SGTIN`
        """
        if isinstance(item_reference, str):
            try:
                item_reference = int(item_reference)
            except ValueError:
                raise AttributeError('item_reference must be an integer')

        self._item_reference = item_reference
        return self

    def serial_number(self, serial_number):
        """
        The Serial Number, assigned by the managing entity to an individual object. The serial
        number is not part of the GTIN, but is formally a part of the SGTIN.

        :param serial_number: The serial number.
        :type serial_number: str, int

        :raises AttributeError: Serial number bit length incorrect.
        :raises AttributeError: Serial number length incorrect.

        :return: The SGTIN tag object.
        :rtype: :class:`epc.schemes.SGTIN`
        """
        if isinstance(serial_number, int):
            if not (serial_number.bit_length() >= 0 and serial_number.bit_length() <= 112):
                raise AttributeError(
                    'Serial number bit length must be be between 0 and 112 (inclusive)'
                )
        elif isinstance(serial_number, str):
            if not (len(serial_number) >= 1 and len(serial_number) <= 16):
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
        Decode an encoded tag and populate this object's values from it.

        :param hex_string: Tag data encoded as a hexadecimal string.
        :type hex_string: str

        :raises ValueError: EPC scheme header does not match input.
        :raises ValueError: Filter does not match allowed values.
        :raises ValueError: Supplied ``hex_string`` bit length invalid.
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
        if partition not in _sgtin_partition_table.keys():
            raise ValueError('Partition `%s` does not match allowed values: %s' % (
                partition, _sgtin_partition_table.keys()
            ))

        # Read tag size, determine positions of elements
        prefix_bit_length, self._company_prefix_length, type_bit_length = \
            _sgtin_partition_table[partition]
        self._item_reference_length = _sgtin_prefix_table[self._company_prefix_length][2]

        # Decode partition elements
        self._company_prefix, self._item_reference = decode_partition(
            tag_binary, prefix_bit_length, type_bit_length, start_pos=14
        )

        # Decode serial
        serial_start = 58
        if self._tag_size == self.SIZE_96:
            serial_length = 38
            self._serial = decode_int(tag_binary[serial_start:serial_start + serial_length])
        elif self._tag_size == self.SIZE_198:
            serial_length = 140
            self._serial = decode_string(tag_binary[serial_start:serial_start + serial_length])

    def decode_gtin(self, gtin, company_prefix_length, serial_number=0):
        """
        Decode a GTIN (Supports GTIN-14, GTIN-13, GTIN-12 formats) to populate this object's
        values from it. Check digit must be included.

        :param gtin: Global trade item number
        :type gtin: str

        :param company_prefix_length: Number of digits of the company prefix length
        :type company_prefix_length: int

        :param serial_number: Serial number to set on the tag. Defaults to `0`.
        :type serial_number: int, str, optional

        :raises ValueError: Invalid GTIN length
        :raises AttributeError: Invalid check digit
        :raises AttributeError: Invalid company_prefix_length specified
        :raises AttributeError: Invalid item_reference in gtin
        """
        if len(gtin) < 12:
            raise ValueError('Invalid GTIN length')

        if len(gtin) != 14:
            # Zero pad GTIN-13 and 12 formats
            gtin = gtin.zfill(14)

        company_prefix_end = company_prefix_length + 1
        item_reference_length = _sgtin_prefix_table[company_prefix_length][2]
        item_reference_end = item_reference_length + company_prefix_end - 1

        try:
            indicator_digit = int(gtin[0:1])
            company_prefix = gtin[1:company_prefix_end]

            if item_reference_length > 1:
                item_reference = int(gtin[company_prefix_end:item_reference_end])
                item_reference = '{}{:0{}d}'.format(
                    indicator_digit, item_reference, item_reference_length - 1)
            else:
                item_reference = str(indicator_digit)

            check_digit = int(gtin[-1:])
            valid_check_digit = self.calc_check_digit(gtin[:-1], '', '')

            if check_digit != valid_check_digit:
                raise AttributeError('Invalid check digit (found %s, expected %s)' % (
                    check_digit, valid_check_digit))
        except IndexError:
            raise AttributeError('Invalid gtin length, or wrong company_prefix_length specified')
        except ValueError:
            raise AttributeError('Invalid item_reference in gtin')

        try:
            serial_number = int(serial_number)
        except ValueError:
            # Serial number is a string, set the encoding to SGTIN-198.
            self._tag_size = self.SIZE_198

        self.company_prefix(company_prefix, company_prefix_length)
        self.item_reference(item_reference)
        self.serial_number(serial_number)

    def decode_barcode(self, barcode, company_prefix_length):
        """
        Decode a barcode and populate this object's values from it.

        :param hex_string: Barcode
        :type hex_string: str

        :param company_prefix_length: Number of digits of the company prefix length
        :type company_prefix_length: int

        :raises ValueError: Expected barcode header does not match input
        :raises AttributeError: Invalid check digit
        :raises AttributeError: Invalid barcode length, or wrong company prefix
        :raises AttributeError: Invalid item_reference in barcode
        """
        if barcode[:2] != self.HEADER_BARCODE:
            raise ValueError(
                'Barcode header does not match expected value: %s' % self.HEADER_BARCODE
            )

        company_prefix_end = company_prefix_length + 3
        item_reference_length = _sgtin_prefix_table[company_prefix_length][2]
        item_reference_end = item_reference_length + company_prefix_end - 1
        check_digit_end = item_reference_end + 1

        try:
            indicator_digit = int(barcode[2:3])
            company_prefix = barcode[3:company_prefix_end]

            if item_reference_length > 1:
                item_reference = int(barcode[company_prefix_end:item_reference_end])
                item_reference = '{}{:0{}d}'.format(
                    indicator_digit, item_reference, item_reference_length - 1)
            else:
                item_reference = str(indicator_digit)

            check_digit = int(barcode[item_reference_end:check_digit_end])
            valid_check_digit = self.calc_check_digit(
                indicator_digit, company_prefix, item_reference[1:])

            if check_digit != valid_check_digit:
                raise AttributeError('Invalid check digit (found %s, expected %s)' % (
                    check_digit, valid_check_digit))

            serial_number = barcode[check_digit_end + 2:]
        except IndexError:
            raise AttributeError('Invalid barcode length, or wrong company_prefix_length specified')
        except ValueError:
            raise AttributeError('Invalid item_reference in barcode')

        try:
            serial_number = int(serial_number)
        except ValueError:
            # Serial number is a string, set the encoding to SGTIN-198.
            self._tag_size = self.SIZE_198

        self.company_prefix(company_prefix, company_prefix_length)
        self.item_reference(item_reference)
        self.serial_number(serial_number)

    def calc_check_digit(self, indicator_digit, company_prefix, item_reference):
        check_string = str(indicator_digit) + str(company_prefix) + str(item_reference)
        evens = []
        odds = []

        for i, char in enumerate(check_string):
            if (i + 2) % 2 == 0:
                # The GTIN check digit calculation digit position is offset by 1,
                # hence we add 2 to i, unlike other schemes.
                evens.append(int(char))
            else:
                odds.append(int(char))

        return (10 - (((3 * sum(evens)) + sum(odds)) % 10)) % 10

    def check_fields(self):
        """
        Checks to make sure all components of the tag are present, including ``size``,
        ``filter``, ``company_prefix``, ``item_reference`` and ``serial_number``.

        :raises AttributeError: If any components of the tag are missing.
        """
        super().check_fields()
        if self._tag_size is None:
            raise AttributeError('Tag size not specified')
        if self._tag_filter is None:
            raise AttributeError('Tag filter not specified')
        if self._company_prefix is None:
            raise AttributeError('Company prefix not specified')
        if self._item_reference is None:
            raise AttributeError('Item reference not specified')
        if self._serial is None:
            raise AttributeError('Serial number not specified')

from epc.encoding import (
    decode_int, encode_int, decode_partition, encode_partition,
    decode_string, encode_string, is_encodable_string, url_encode_string
)

from .base import EpcScheme

_sgln_partition_table = {
    # Partition Value: (Company Prefix Length (bits),
    #                   Company Prefix Length (digits),
    #                   Location Reference Length (bits))
    0: (40, 12, 1),
    1: (37, 11, 4),
    2: (34, 10, 7),
    3: (30, 9, 11),
    4: (27, 8, 14),
    5: (24, 7, 17),
    6: (20, 6, 21),
}

_sgln_prefix_table = {
    # Company Prefix Length (digits): (Partition Value,
    #                                  Location Reference Length (bits)
    #                                  Location Reference Length (digits))
    12: (0, 1, 0),
    11: (1, 4, 1),
    10: (2, 7, 2),
    9: (3, 11, 3),
    8: (4, 14, 4),
    7: (5, 17, 5),
    6: (6, 21, 6),
}


class SGLN(EpcScheme):
    """
    The SGLN EPC scheme is used to assign a unique identity to a physical location, such as a
    specific building or a specific unit of shelving within a warehouse.

    General syntax:
    urn:epc:id:sgln:CompanyPrefix.LocationReference.Extension

    Example:
    urn:epc:id:sgln:0614141.12345.400
    """
    SGLN_96 = 'sgln-96'
    SGLN_195 = 'sgln-195'

    ENCODINGS = (
        SGLN_96, SGLN_195
    )

    HEADER_96 = 0x32
    HEADER_195 = 0x39
    HEADER_BARCODE = '414'
    HEADERS = (
        HEADER_96, HEADER_195
    )

    SIZE_96 = 96
    SIZE_195 = 208  # While the size is really 195, set to 208 because we need a multiple of 16
    TAG_SIZES = (
        SIZE_96, SIZE_195
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

    _location_reference = None
    _location_reference_length = None
    _extension = None

    def __init__(self, *args, **kwargs):
        self._tag_size = self.SIZE_96
        self._tag_filter = self.FILTER_ALL
        super().__init__(*args, **kwargs)

    def __int__(self):
        self.check_fields()

        partition, reference_bit_length, refrence_digits = \
            _sgln_prefix_table[self._company_prefix_length]
        prefix_bit_length = _sgln_partition_table[partition][0]

        content = encode_partition(
            partition,
            self._company_prefix, prefix_bit_length,
            self._location_reference, reference_bit_length, d_digits=refrence_digits
        )

        if self._tag_size == self.SIZE_96:
            header = self.HEADER_96
            extension = encode_int(self._extension, bit_length=41)
        elif self._tag_size == self.SIZE_195:
            header = self.HEADER_195
            extension = encode_string(self._extension, bit_length=140)

        return int('{header:08b}{tag_filter:03b}{content}{extension}{padding}'.format(
            header=header, tag_filter=self._tag_filter, content=content, extension=extension,
            padding=('0' * 13 if self._tag_size == self.SIZE_195 else ''),
        ), 2)

    @property
    def pure_identity_uri(self):
        """
        :return: The tag's pure identity URI.
        :rtype: str
        """
        self.check_fields()

        if self._location_reference_length > 0:
            location_reference = '{:0{}d}'.format(
                self._location_reference, self._location_reference_length)
        else:
            location_reference = ''

        if self._tag_size == self.SIZE_96:
            extension = self._extension
        elif self._tag_size == self.SIZE_195:
            extension = url_encode_string(self._extension)

        return 'urn:epc:id:sgln:' \
               '{_company_prefix:0{_company_prefix_length}d}.' \
               '{location_reference}.{extension}'.format(
                    location_reference=location_reference, extension=extension, **self.__dict__
                )

    @property
    def tag_uri(self):
        """
        :return: The tag's URI.
        :rtype: str
        """
        self.check_fields()

        if self._location_reference_length > 0:
            location_reference = '{:0{}d}'.format(
                self._location_reference, self._location_reference_length)
        else:
            location_reference = ''

        if self._tag_size == self.SIZE_96:
            extension = self._extension
        elif self._tag_size == self.SIZE_195:
            extension = url_encode_string(self._extension)

        return 'urn:epc:tag:{encoding}:{_tag_filter}.' \
               '{_company_prefix:0{_company_prefix_length}d}.' \
               '{location_reference}.{extension}'.format(
                    encoding=self.encoding, location_reference=location_reference,
                    extension=extension, **self.__dict__
                )

    @property
    def barcode(self):
        """
        :return: The barcode representation of the tag.
        :rtype: str
        """
        self.check_fields()

        check_digit = self.calc_check_digit()
        gln = '{_company_prefix:0{_company_prefix_length}d}' \
              '{_location_reference:0{_location_reference_length}d}{check_digit}'.format(
                    check_digit=check_digit, **self.__dict__
                )

        return '{header}{gln}254{_extension}'.format(
            header=self.HEADER_BARCODE, gln=gln, **self.__dict__
        )

    @property
    def barcode_humanized(self):
        """
        :return: A human readable barcode representation of the tag.
        :rtype: str
        """
        self.check_fields()

        check_digit = self.calc_check_digit()
        gln = '{_company_prefix:0{_company_prefix_length}d}' \
              '{_location_reference:0{_location_reference_length}d}{check_digit}'.format(
                    check_digit=check_digit, **self.__dict__
                )

        return '({header}){gln}(254){_extension}'.format(
            header=self.HEADER_BARCODE, gln=gln, **self.__dict__
        )

    @property
    def encoding(self):
        encoding = None
        if self._tag_size == self.SIZE_96:
            encoding = self.SGLN_96
        elif self._tag_size == self.SIZE_195:
            encoding = self.SGLN_195
        return encoding

    @property
    def values(self):
        """
        :return: Dictionary containing:

            * ``size`` (int): the tag's size in bits

            * ``filter`` (int)

            * ``company_prefix`` (str)

            * ``location_reference`` (int)

            * ``extension`` (int *or* str)
        """
        return {
            'size': self._tag_size,
            'filter': self._tag_filter,
            'company_prefix': '{:0{}d}'.format(self._company_prefix, self._company_prefix_length),
            'location_reference': '{:0{}d}'.format(
                self._location_reference, self._location_reference_length),
            'extension': self._extension,
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

        Allowed values for SGLN tags:

        +-------+-------------------+--------------+
        | Value | Constant          | Description  |
        +=======+===================+==============+
        | 0     | FILTER_ALL        | All Others   |
        +-------+-------------------+--------------+
        | 1-7   | FILTER_RESERVED_* | Reserved     |
        +-------+-------------------+--------------+

        :param tag_filter: The filter value, defaults to ``FILTER_ALL``.
        :type tag_filter: int

        :raises AttributeError: Filter must be between 0 and 7.

        :return: The SGLN tag object.
        :rtype: :class:`epc.schemes.SGLN`
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

        :param company_prefix: GS1 company prefix.
        :type company_prefix: str, int

        :param company_prefix_length: Number of digits in the company prefix.
            Required when ``company_prefix`` is an int.
        :type company_prefix_length: int, optional

        :return: The SGLN tag object.
        :rtype: :class:`epc.schemes.SGLN`
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
        self._location_reference_length = _sgln_prefix_table[self._company_prefix_length][2]
        return self

    def location_reference(self, location_reference):
        """
        The Location Reference, assigned uniquely by the managing entity to a specific
        physical location.

        :param location_reference: The location reference
        :type location_reference: int, str

        :raises ValueError: Unable to convert input to an integer.

        :return: The SGLN tag object.
        :rtype: :class:`epc.schemes.SGLN`
        """
        if isinstance(location_reference, str):
            try:
                location_reference = int(location_reference)
            except ValueError:
                raise AttributeError('location_reference must be an integer')

        self._location_reference = location_reference
        return self

    def extension(self, extension):
        """
        The GLN Extension, assigned by the managing entity to an individual unique location. If the
        entire GLN Extension is just a single zero digit, it indicates that the SGLN stands for a
        GLN, without an extension.

        :param extension: The GLN extension
        :type extension: str, int

        :raises AttributeError: Extension length incorrect.

        :return: The SGLN tag object.
        :rtype: :class:`epc.schemes.SGLN`
        """
        if isinstance(extension, str):
            if self._tag_size == self.SIZE_96:
                extension = int(extension)
            elif self._tag_size == self.SIZE_195:
                if len(extension) > 21:
                    raise AttributeError('Extension length must less than 21 characters.')

                is_encodable_string(extension, raise_exception=True)

        self._extension = extension
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

        # Read partition
        partition = decode_int(tag_binary[11:14])
        if partition not in _sgln_partition_table.keys():
            raise ValueError('Partition `%s` does not match allowed values: %s' % (
                partition, _sgln_partition_table.keys()
            ))

        # Read tag size, determine positions of elements
        prefix_bit_length, self._company_prefix_length, location_reference_bit_length = \
            _sgln_partition_table[partition]

        self._location_reference_length = _sgln_prefix_table[self._company_prefix_length][2]

        # Decode partition elements
        self._company_prefix, self._location_reference = decode_partition(
            tag_binary, prefix_bit_length, location_reference_bit_length, start_pos=14
        )

        # Decode extension
        if self._tag_size == self.SIZE_96:
            self._extension = decode_int(tag_binary[55:])
        elif self._tag_size == self.SIZE_195:
            self._extension = decode_string(tag_binary[55:])

    def decode_barcode(self, barcode, company_prefix_length):
        """
        Decode a barcode and populate this object's values from it.

        :param hex_string: Barcode
        :type hex_string: str

        :param company_prefix_length: Number of digits of the company prefix length
        :type company_prefix_length: int

        :raises ValueError: Expected barcode header does not match input.
        :raises AttributeError: Invalid barcode length, or wrong company prefix.
        """
        if barcode[:3] != self.HEADER_BARCODE:
            raise ValueError(
                'Barcode header does not match expected value: %s' % self.HEADER_BARCODE
            )

        company_prefix_end = company_prefix_length + 3
        location_reference_length = _sgln_prefix_table[company_prefix_length][2]
        location_reference_end = location_reference_length + company_prefix_end
        check_digit_end = location_reference_end + 1

        try:
            company_prefix = barcode[3:company_prefix_end]

            if location_reference_length > 0:
                location_reference = int(barcode[company_prefix_end:location_reference_end])
            else:
                location_reference = 0

            check_digit = int(barcode[location_reference_end:check_digit_end])

            self.company_prefix(company_prefix, company_prefix_length)
            self.location_reference(location_reference)

            if check_digit != self.calc_check_digit():
                raise AttributeError('Invalid check digit (found %s, expected %s)' % (
                    check_digit, self.calc_check_digit()
                ))

            extension = barcode[check_digit_end + 3:]
        except IndexError:
            raise AttributeError('Invalid barcode length, or wrong company_prefix_length specified')
        except ValueError:
            raise AttributeError('Invalid asset reference in barcode')

        try:
            extension = int(extension)
        except ValueError:
            # Extension is a string, set the encoding to SGLN-195.
            self._tag_size = self.SIZE_195

        self.company_prefix(company_prefix, company_prefix_length)
        self.location_reference(location_reference)
        self.extension(extension)

    def calc_check_digit(self):
        check_string = \
            '{_company_prefix:0{_company_prefix_length}d}' \
            '{_location_reference:0{_location_reference_length}d}'.format(**self.__dict__)
        evens = []
        odds = []

        for i, char in enumerate(check_string):
            if (i + 1) % 2 == 0:
                evens.append(int(char))
            else:
                odds.append(int(char))

        return (10 - (((3 * sum(evens)) + sum(odds)) % 10)) % 10

    def check_fields(self):
        """
        Checks to make sure all components of the tag are present, including ``size``,
        ``filter``, ``company_prefix``, ``location_reference`` and ``extension``.

        :raises AttributeError: If any components of the tag are missing.
        """
        super().check_fields()
        if self._tag_size is None:
            raise AttributeError('Tag size not specified')
        if self._tag_filter is None:
            raise AttributeError('Tag filter not specified')
        if self._company_prefix is None:
            raise AttributeError('Company prefix not specified')
        if self._location_reference is None:
            raise AttributeError('Location reference not specified')
        if self._extension is None:
            raise AttributeError('Extention not specified')

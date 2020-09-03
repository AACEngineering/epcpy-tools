from epc.encoding import (
    decode_int, decode_partition, encode_partition,
    is_encodable_string, url_encode_string,
    decode_string_partition, encode_string_partition
)

from .base import EpcScheme

_giai_96_partition_table = {
    # Partition Value: (Company Prefix Length (bits),
    #                   Company Prefix Length (digits),
    #                   Asset Reference Length (bits))
    0: (40, 12, 42),
    1: (37, 11, 45),
    2: (34, 10, 48),
    3: (30, 9, 52),
    4: (27, 8, 55),
    5: (24, 7, 58),
    6: (20, 6, 62),
}

_giai_96_prefix_table = {
    # Company Prefix Length (digits): (Partition Value,
    #                                  Asset Reference Length (bits)
    #                                  Asset Reference Length (max digits))
    12: (0, 42, 13),
    11: (1, 45, 14),
    10: (2, 48, 15),
    9: (3, 52, 16),
    8: (4, 55, 17),
    7: (5, 58, 18),
    6: (6, 62, 19),
}

_giai_202_partition_table = {
    # Partition Value: (Company Prefix Length (bits),
    #                   Company Prefix Length (digits),
    #                   Asset Reference Length (bits))
    0: (40, 12, 148),
    1: (37, 11, 151),
    2: (34, 10, 154),
    3: (30, 9, 158),
    4: (27, 8, 161),
    5: (24, 7, 164),
    6: (20, 6, 168),
}

_giai_202_prefix_table = {
    # Company Prefix Length (digits): (Partition Value,
    #                                  Asset Reference Length (bits)
    #                                  Asset Reference Length (max characters))
    12: (0, 148, 18),
    11: (1, 151, 19),
    10: (2, 154, 20),
    9: (3, 158, 21),
    8: (4, 161, 22),
    7: (5, 164, 23),
    6: (6, 168, 24),
}


class GIAI(EpcScheme):
    """
    The Global Individual Asset Identifier EPC scheme is used to assign a unique identity
    to a specific asset, such as a forklift or a computer.

    The scheme supports two sizes: 96 bit and 202 bit tags.
    Alphanumeric character are supported on the larger size tag for the asset reference.

    General syntax:
    urn:epc:id:giai:CompanyPrefix.IndividualAssetReference

    Example:
    urn:epc:id:giai:0614141.1234540

    :param epc: Hexadecimal EPC tag data
    :type epc: str, optional

    :param barcode: GIAI barcode data
    :type barcode: str, optional

    :param company_prefix_length: Number of digits in the company prefix.
        Required when specifying a barcode.
    :type company_prefix_length: int, optional
    """
    GIAI_96 = 'giai-96'
    GIAI_202 = 'giai-202'
    ENCODINGS = (
        GIAI_96, GIAI_202
    )

    HEADER_96 = 0x34
    HEADER_202 = 0x38
    HEADER_BARCODE = '8004'
    HEADERS = (
        HEADER_96, HEADER_202
    )

    SIZE_96 = 96
    SIZE_202 = 208  # While the size is really 202, set to 208 because we need a multiple of 16.
    TAG_SIZES = (
        SIZE_96,
        SIZE_202,
    )

    FILTER_ALL = 0
    FILTER_RAIL = 1
    FILTER_RESERVED_2 = 2
    FILTER_RESERVED_3 = 3
    FILTER_RESERVED_4 = 4
    FILTER_RESERVED_5 = 5
    FILTER_RESERVED_6 = 6
    FILTER_RESERVED_7 = 7
    FILTERS = (
        (FILTER_ALL, 'All Others'),
        (FILTER_RAIL, 'Rail Vehicle'),
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
    _asset_reference = None

    def __init__(self, *args, **kwargs):
        self._tag_size = self.SIZE_96
        self._tag_filter = self.FILTER_ALL
        super().__init__(*args, **kwargs)

    def __int__(self):
        self.check_fields()

        if self._tag_size == self.SIZE_96:
            partition, reference_bit_length, _ = _giai_96_prefix_table[self._company_prefix_length]
            prefix_bit_length = _giai_96_partition_table[partition][0]
            header = self.HEADER_96

            content = encode_partition(
                partition,
                self._company_prefix, prefix_bit_length,
                self._asset_reference, reference_bit_length
            )

            return int('{header:08b}{tag_filter:03b}{content}'.format(
                header=header, tag_filter=self._tag_filter, content=content
            ), 2)

        elif self._tag_size == self.SIZE_202:
            partition, reference_bit_length, _ = _giai_202_prefix_table[self._company_prefix_length]
            prefix_bit_length = _giai_202_partition_table[partition][0]
            header = self.HEADER_202

            content = encode_string_partition(
                partition,
                self._company_prefix, prefix_bit_length,
                self._asset_reference, reference_bit_length
            )

            return int('{header:08b}{tag_filter:03b}{content}{padding}'.format(
                header=header, content=content, tag_filter=self._tag_filter, padding='0' * 6
            ), 2)

    @property
    def pure_identity_uri(self):
        """
        :return: The tag's pure identity URI.
        :rtype: str
        """
        self.check_fields()
        if self._tag_size == self.SIZE_96:
            asset_reference = self._asset_reference
        elif self._tag_size == self.SIZE_202:
            asset_reference = url_encode_string(self._asset_reference)

        return 'urn:epc:id:giai:' \
               '{_company_prefix:0{_company_prefix_length}d}.{asset_reference}'.format(
                    asset_reference=asset_reference, **self.__dict__
                )

    @property
    def tag_uri(self):
        """
        :return: The tag's URI.
        :rtype: str
        """
        self.check_fields()
        if self._tag_size == self.SIZE_96:
            asset_reference = self._asset_reference
        elif self._tag_size == self.SIZE_202:
            asset_reference = url_encode_string(self._asset_reference)

        return 'urn:epc:tag:{encoding}:{_tag_filter}.' \
               '{_company_prefix:0{_company_prefix_length}d}.{asset_reference}'.format(
                    asset_reference=asset_reference, encoding=self.encoding, **self.__dict__
                )

    @property
    def barcode(self):
        """
        :return: The barcode representation of the tag.
        :rtype: str
        """
        self.check_fields()
        return '{header}{_company_prefix:0{_company_prefix_length}d}{_asset_reference}'.format(
            header=self.HEADER_BARCODE, **self.__dict__
        )

    @property
    def barcode_humanized(self):
        """
        :return: A human readable barcode representation of the tag.
        :rtype: str
        """
        self.check_fields()
        return '({header}) {_company_prefix:0{_company_prefix_length}d} {_asset_reference}'.format(
            header=self.HEADER_BARCODE, **self.__dict__
        )

    @property
    def encoding(self):
        encoding = None
        if self._tag_size == self.SIZE_96:
            encoding = self.GIAI_96
        elif self._tag_size == self.SIZE_202:
            encoding = self.GIAI_202
        return encoding

    @property
    def values(self):
        """
        :return: Dictionary containing:

            * ``size`` (int): the tag's size in bits

            * ``filter`` (int)

            * ``company_prefix`` (str)

            * ``asset_reference`` (int *or* str)
        """
        return {
            'size': self._tag_size,
            'filter': self._tag_filter,
            'company_prefix': '{:0{}d}'.format(self._company_prefix, self._company_prefix_length),
            'asset_reference': self._asset_reference,
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

        Allowed values for GIAI tags:

        +-------+-------------------+--------------+
        | Value | Constant          | Description  |
        +=======+===================+==============+
        | 0     | FILTER_ALL        | All Others   |
        +-------+-------------------+--------------+
        | 1     | FILTER_RAIL       | Rail Vehicle |
        +-------+-------------------+--------------+
        | 2-7   | FILTER_RESERVED_* | Reserved     |
        +-------+-------------------+--------------+

        :param tag_filter: The filter value, defaults to ``FILTER_ALL``.
        :type tag_filter: int

        :raises AttributeError: Filter must be between 0 and 7.

        :return: The GIAI tag object.
        :rtype: :class:`epc.schemes.GIAI`
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

        :return: The GIAI tag object.
        :rtype: :class:`epc.schemes.GIAI`
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
        return self

    def asset_reference(self, asset_reference):
        """
        The Individual Asset Reference, assigned uniquely by the managing entity
        to a specific asset.

        :param asset_reference: The asset reference.
        :type asset_reference: str, int

        :raises AttributeError: Reference length must be less than 24 characters.
        :raises ValueError: Reference string character not encodeable.

        :return: The GIAI tag object.
        :rtype: :class:`epc.schemes.GIAI`
        """
        if isinstance(asset_reference, str):
            if len(asset_reference) > 24:
                raise AttributeError('Asset reference length must less than 24 characters.')

            is_encodable_string(asset_reference, raise_exception=True)

        self._asset_reference = asset_reference
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
        if partition not in _giai_96_partition_table.keys():
            raise ValueError('Partition `%s` does not match allowed values: %s' % (
                partition, _giai_96_partition_table.keys()
            ))

        # Read tag size, determine positions of elements
        if self._tag_size == self.SIZE_96:
            prefix_bit_length, self._company_prefix_length, asset_bit_length = \
                _giai_96_partition_table[partition]
            decoder = decode_partition
        elif self._tag_size == self.SIZE_202:
            prefix_bit_length, self._company_prefix_length, asset_bit_length = \
                _giai_202_partition_table[partition]
            decoder = decode_string_partition

        # Decode partition elements
        self._company_prefix, self._asset_reference = decoder(
            tag_binary, prefix_bit_length, asset_bit_length, start_pos=14
        )

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
        if barcode[:4] != self.HEADER_BARCODE:
            raise ValueError(
                'Barcode header does not match expected value: %s' % self.HEADER_BARCODE
            )

        try:
            company_prefix = barcode[4:4 + company_prefix_length]
            asset_reference = barcode[company_prefix_length + 4:]
            asset_reference = int(asset_reference)
        except IndexError:
            raise AttributeError('Invalid barcode length, or wrong company_prefix_length specified')
        except ValueError:
            # Asset reference must be a string, set the encoding to GIAI-202.
            self._tag_size = self.SIZE_202

        self.company_prefix(company_prefix, company_prefix_length)
        self.asset_reference(asset_reference)

    def check_fields(self):
        """
        Checks to make sure all components of the tag are present, including ``size``,
        ``filter``, ``company_prefix`` and ``asset_reference``.

        :raises AttributeError: If any components of the tag are missing.
        """
        super().check_fields()
        if self._tag_size is None:
            raise AttributeError('Tag size not specified')
        if self._tag_filter is None:
            raise AttributeError('Tag filter not specified')
        if self._company_prefix is None:
            raise AttributeError('Company prefix not specified')
        if self._asset_reference is None:
            raise AttributeError('Asset reference not specified')

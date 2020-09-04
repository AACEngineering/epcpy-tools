from epc.encoding import encode_int


class EpcScheme:
    """
    Abstract class used to implement an EPC (electronic product code) scheme.

    To implement a new scheme, an __int__ method that represents the EPC in an integer
    format must be implemented that can be written into EPC memory portion of an RFID tag.
    """
    ENCODINGS = ()
    HEADERS = ()
    TAG_SIZES = ()

    HEADER_BARCODE = None

    _tag_size = None

    def __init__(self, epc=None, barcode=None, company_prefix_length=None):
        if epc is not None:
            self.decode_epc(epc)
        elif barcode is not None:
            self.decode_barcode(barcode, company_prefix_length)

    def __str__(self):
        return self.pure_identity_uri

    def __int__(self):
        raise NotImplementedError

    def __index__(self):
        return self.__int__()

    def __repr__(self):
        try:
            return '<%s %s>' % (self.__class__.__module__, self.__str__())
        except AttributeError:
            return '<%s>' % self.__class__.__module__

    @property
    def pure_identity_uri(self):
        raise NotImplementedError

    @property
    def tag_uri(self):
        raise NotImplementedError

    @property
    def barcode(self):
        raise NotImplementedError

    @property
    def barcode_humanized(self):
        raise NotImplementedError

    @property
    def encoding(self):
        raise NotImplementedError

    @property
    def values(self):
        return {
            'tag_size': self._tag_size,
        }

    def tag_size(self, tag_size):
        """
        Set the size for the tag.

        :param tag_size: Tag size in bits.
        :type tag_size: int

        :raises AttributeError: Invalid tag size specified.
        """
        if tag_size not in self.TAG_SIZES:
            raise AttributeError(
                'Invalid tag size specified, valid options are: %s', self.TAG_SIZES
            )

        self._tag_size = tag_size
        return self

    def check_fields(self):
        """
        Check required fields (tag size, other)

        Override and call super() on derrived classes.
        """
        if not len(self.ENCODINGS) >= 1:
            raise NotImplementedError(
                'ENCODINGS must be specified with one or more elements on derrived classes.'
            )

        if not len(self.HEADERS) >= 1:
            raise NotImplementedError(
                'HEADERS must be specified with one or more elements on derrived classes.'
            )

        if not len(self.TAG_SIZES) >= 1:
            raise NotImplementedError(
                'TAG_SIZES must be specified with one or more elements on derrived classes.'
            )

    def decode_epc(self, hex_string):
        """
        Decode an EPC hex string and populate the values in the scheme.

        This function returns a binary string of the tag for parsing.

        You must override this method on each scheme implementation.
        """
        tag_data = int(hex_string, 16)
        tag_length = tag_data.bit_length()

        # Pad the length to multiples of 16, per the EPC Tag Data Standard
        if tag_length % 16 != 0:
            tag_length += 16 - tag_length % 16

        if tag_length not in self.TAG_SIZES:
            raise ValueError('Invalid number of bits in tag (%s), valid options are: %s' % (
                tag_length, self.TAG_SIZES
            ))

        self._tag_size = tag_length
        return encode_int(tag_data, tag_length)

    def decode_barcode(self, barcode, company_prefix_length):
        """
        Decode a barcode string and populate values in the scheme.
        """
        raise NotImplementedError

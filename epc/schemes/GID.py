from epc.encoding import decode_int

from .base import EpcScheme


class GID(EpcScheme):
    """
    The General Identifier EPC scheme is independent of any specifications or identity scheme
    outside the EPC global Tag Data Standard.

    General syntax:
    urn:epc:id:gid:ManagerNumber.ObjectClass.SerialNumber

    Example:
    urn:epc:id:gid:95100000.12345.400

    :param epc: Hexadecimal EPC tag data
    :type epc: str, optional
    """
    GID_96 = 'gid-96'
    ENCODINGS = (
        GID_96,
    )

    HEADER_96 = 0x35
    HEADERS = (
        HEADER_96,
    )

    SIZE_96 = 96
    TAG_SIZES = (
        SIZE_96,
    )

    _tag_size = None
    _manager_number = None
    _object_class = None
    _serial_number = None

    def __init__(self, *args, **kwargs):
        self._tag_size = self.SIZE_96
        super().__init__(*args, **kwargs)

    def __int__(self):
        """
        :returns: The GID encoded numeric tag data.
        :rtype: int

        This is a built-in python method, and shouldn't be called directly.
        """
        self.check_fields()
        return int('{header:x}{_manager_number:07x}{_object_class:06x}{_serial_number:09x}'.format(
            header=self.HEADER_96, **self.__dict__
        ), 16)

    @property
    def pure_identity_uri(self):
        """
        :return: The tag's pure identity URI.
        :rtype: str
        """
        self.check_fields()
        return 'urn:epc:id:gid:{_manager_number}.{_object_class}.{_serial_number}'.format(
            **self.__dict__
        )

    @property
    def tag_uri(self):
        """
        :return: The tag's URI.
        :rtype: str
        """
        self.check_fields()
        return 'urn:epc:tag:gid-96:{_manager_number}.{_object_class}.{_serial_number}'.format(
            **self.__dict__
        )

    @property
    def barcode(self):
        """Barcodes are not supported by the GID scheme."""
        return None

    @property
    def barcode_humanized(self):
        """Barcodes are not supported by the GID scheme."""
        return None

    @property
    def encoding(self):
        encoding = None
        if self._tag_size == self.SIZE_96:
            encoding = self.GID_96
        return encoding

    @property
    def values(self):
        """
        :return: Dictionary containing:

            * ``size`` (int): the tag's size in bits

            * ``manager_number`` (int)

            * ``object_class`` (int)

            * ``serial_number`` (int)
        """
        return {
            'size': self._tag_size,
            'manager_number': self._manager_number,
            'object_class': self._object_class,
            'serial_number': self._serial_number,
        }

    def manager_number(self, manager_number):
        """
        Set the manager number data for the tag.

        The General Manager Number identifies an organizational entity (essentially a company,
        manager or other organization) that is responsible for maintaining the numbers in subsequent
        fields – Object Class and Serial Number.

        GS1 assigns the General Manager Number to an entity,
        and ensures that each General Manager Number is unique. Note that a General Manager
        Number is not a GS1 Company Prefix. A General Manager Number may only be used in GID EPCs.

        :param manager_number: GS1 manager number.
        :type manager_number: str, int

        :raises ValueError: Unable to convert string to an integer.
        :raises AttributeError: Input outside valid range (0 to 268435455).

        :return: The GID tag object.
        :rtype: :class:`epc.schemes.GID`
        """
        if isinstance(manager_number, str):
            try:
                manager_number = int(manager_number)
            except ValueError:
                raise AttributeError('manager_number must be an integer')

        if not (manager_number >= 0 and manager_number <= 268435455):
            raise AttributeError(
                'Manager number must be between 0 and 268435455 (inclusive)'
            )

        self._manager_number = manager_number
        return self

    def object_class(self, object_class):
        """
        Set the object class data for the tag.

        The Object Class is used by an EPC managing entity to identify a class or “type” of thing.
        These object class numbers, of course, must be unique within
        each General Manager Number domain.

        :param object_class: Numeric object class.
        :type object_class: str, int

        :raises ValueError: Unable to convert string to an integer.
        :raises AttributeError: Input outside valid range (0 to 16777215).

        :return: The GID tag object.
        :rtype: :class:`epc.schemes.GID`
        """
        if isinstance(object_class, str):
            try:
                object_class = int(object_class)
            except ValueError:
                raise AttributeError('object_class must be an integer')

        if not (object_class >= 0 and object_class <= 16777215):
            raise AttributeError(
                'Object class must be between 0 and 16777215 (inclusive)'
            )

        self._object_class = object_class
        return self

    def serial_number(self, serial_number):
        """
        Set the serial number data for the tag.

        The Serial Number code, or serial number, is unique within each object class. In other
        words, the managing entity is responsible for assigning unique, non-repeating serial numbers
        for every instance within each object class.

        :param serial_number: Numeric serial number.
        :type serial_number: str, int

        :raises ValueError: Unable to convert string to an integer.
        :raises AttributeError: Input outside valid range (0 and 68719476735).

        :return: The GID tag object.
        :rtype: :class:`epc.schemes.GID`
        """
        if isinstance(serial_number, str):
            try:
                serial_number = int(serial_number)
            except ValueError:
                raise AttributeError('serial_number must be an integer')

        if not (serial_number >= 0 and serial_number <= 68719476735):
            raise AttributeError(
                'Serial number must be between 0 and 68719476735 (inclusive)'
            )

        self._serial_number = serial_number
        return self

    def decode_epc(self, hex_string):
        """
        Decode an encoded tag and populate this object's values from it.

        :param hex_string: Tag data encoded as a hexadecimal string.
        :type hex_string: str

        :raises ValueError: EPC scheme header does not match input.
        :raises ValueError: Supplied ``hex_string`` bit length invalid.
        """
        tag_binary = super().decode_epc(hex_string)

        # Verify header
        header = decode_int(tag_binary[0:8])
        if header != self.HEADER_96:
            raise ValueError(
                'Header `{:#04x}` does not match allowed values: ({:#04x}).'.format(
                    header, self.HEADER_96
                )
            )

        # Decode values
        self._manager_number = decode_int(tag_binary[8:36])
        self._object_class = decode_int(tag_binary[36:60])
        self._serial_number = decode_int(tag_binary[60:96])

    def decode_barcode(self, *args, **kwargs):
        raise NotImplementedError('This epc scheme does not support barcodes')

    def check_fields(self):
        """
        Checks to make sure all components of the tag are present, including ``size``,
        ``manager_number``, ``object_class`` and ``serial_number``.

        :raises AttributeError: If any components of the tag are missing.
        """
        super().check_fields()
        if self._tag_size is None:
            raise AttributeError('Tag size not specified')
        if self._manager_number is None:
            raise AttributeError('Manager number not specified')
        if self._object_class is None:
            raise AttributeError('Object class not specified')
        if self._serial_number is None:
            raise AttributeError('Serial number not specified')

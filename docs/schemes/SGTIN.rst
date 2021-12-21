SGTIN
-----

.. autoclass:: epc.schemes.SGTIN
    
    .. automethod:: filter

    .. automethod:: company_prefix

    .. automethod:: item_reference

    .. automethod:: serial_number    

    .. method:: tag_size

        Set the size for the tag. Options are ``SIZE_96`` or ``SIZE_198``.

        :param tag_size: Tag size in bits. Defaults to ``SIZE_96``.
        :type tag_size: int

        :raises AttributeError: Invalid tag size specified.

        :return: The SGTIN tag object.
        :rtype: :class:`epc.schemes.SGTIN`

    .. autoproperty:: tag_uri

    .. autoproperty:: pure_identity_uri

    .. autoproperty:: barcode

    .. autoproperty:: barcode_humanized

    .. autoproperty:: gtin

    .. autoproperty:: values

    .. automethod:: decode_epc

    .. automethod:: decode_barcode

    .. automethod:: decode_gtin

    .. automethod:: check_fields    

.. hint::

    To get the encoded tag data, use python's built in conversion methods:

    .. code-block:: python
        :emphasize-lines: 5, 9

        >>> tag = SGTIN().tag_size(SGTIN.SIZE_198)
        >>> tag.company_prefix('000123').item_reference(18).serial_number('ABC')

        # Hexadecimal
        >>> hex(tag)
        '0x3618001ec00004a0c28600000000000000000000000000000000'

        # Binary
        >>> bin(tag)
        '0b11011000011000000000000001111011000000000000000000010010100000110000101000011000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'


Constants
^^^^^^^^^

Filters

.. data:: SGTIN.FILTER_ALL

.. data:: SGTIN.FILTER_POS

.. data:: SGTIN.FILTER_FULL_CASE

.. data:: SGTIN.FILTER_RESERVED_3

.. data:: SGTIN.FILTER_INNER_PACK

.. data:: SGTIN.FILTER_RESERVED_5

.. data:: SGTIN.FILTER_UNIT_LOAD

.. data:: SGTIN.FILTER_INNER_ITEM

Sizes

.. data:: SGTIN.SIZE_96

    96 bit tag size.

.. data:: SGTIN.SIZE_198

    198 bit tag size.

Headers

.. data:: SGTIN.HEADER_BARCODE

    GS1 specified GTIN barcode header: ``01``.

.. data:: SGTIN.HEADER_BARCODE_SERIAL_NUMBER

    GS1 specified GTIN serial barcode header: ``21``.

.. data:: SGTIN.HEADER_96

    GS1 specified hexadecimal header for 96 bit SGTIN tags: ``0x30``.

.. data:: SGTIN.HEADER_198

    GS1 specified hexadecimal header for 202 bit SGTIN tags: ``0x36``.


.. data:: SGTIN.SGTIN_96

    Human readable GS1 specified header for 96 bit SGTIN tags: ``sgtin-96``.


.. data:: SGTIN.SGTIN_198

    Human readable GS1 specified header for 198 bit SGTIN tags: ``sgtin-198``.


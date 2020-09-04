GRAI
----

.. autoclass:: epc.schemes.GRAI
    
    .. automethod:: filter

    .. automethod:: company_prefix

    .. automethod:: asset_type

    .. automethod:: serial_number    

    .. method:: tag_size

        Set the size for the tag. Options are ``SIZE_96`` or ``SIZE_170``.

        :param tag_size: Tag size in bits. Defaults to ``SIZE_96``.
        :type tag_size: int

        :raises AttributeError: Invalid tag size specified.

        :return: The GRAI tag object.
        :rtype: :class:`epc.schemes.GRAI`

    .. autoproperty:: tag_uri

    .. autoproperty:: pure_identity_uri

    .. autoproperty:: barcode

    .. autoproperty:: barcode_humanized

    .. autoproperty:: values

    .. automethod:: decode_epc

    .. automethod:: decode_barcode

    .. automethod:: check_fields    

.. hint::

    To get the encoded tag data, use python's built in conversion methods:

    .. code-block:: python
        :emphasize-lines: 5, 9

        >>> tag = GRAI().tag_size(GRAI.SIZE_170)
        >>> tag.company_prefix('000123').asset_type(8).serial_number('ABC')

        # Hexadecimal
        >>> hex(tag)
        '0x3718001ec0000220c286000000000000000000000000'

        # Binary
        >>> bin(tag)
        '0b110111000110000000000000011110110000000000000000000010001000001100001010000110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'


Constants
^^^^^^^^^

Filters

.. data:: GRAI.FILTER_ALL

.. data:: GRAI.FILTER_RESERVED_*

    Replace asterisk with 1-7.

Sizes

.. data:: GRAI.SIZE_96

    96 bit tag size.

.. data:: GRAI.SIZE_170

    170 bit tag size.

Headers

.. data:: GRAI.HEADER_BARCODE

    GS1 specified barcode header: ``8003``.

.. data:: GRAI.HEADER_96

    GS1 specified hexadecimal header for 96 bit GRAI tags: ``0x33``.

.. data:: GRAI.HEADER_170

    GS1 specified hexadecimal header for 202 bit GRAI tags: ``0x37``.


.. data:: GRAI.GRAI_96

    Human readable GS1 specified header for 96 bit GRAI tags: ``grai-96``.


.. data:: GRAI.GRAI_170

    Human readable GS1 specified header for 202 bit GRAI tags: ``grai-170``.


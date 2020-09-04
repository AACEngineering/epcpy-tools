SGLN
----

.. autoclass:: epc.schemes.SGLN
    
    .. automethod:: filter

    .. automethod:: company_prefix

    .. automethod:: location_reference

    .. automethod:: extension    

    .. method:: tag_size

        Set the size for the tag. Options are ``SIZE_96`` or ``SIZE_195``.

        :param tag_size: Tag size in bits. Defaults to ``SIZE_96``.
        :type tag_size: int

        :raises AttributeError: Invalid tag size specified.

        :return: The SGLN tag object.
        :rtype: :class:`epc.schemes.SGLN`

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

        >>> tag = SGLN()
        >>> tag.company_prefix(1234, company_prefix_length=6).location_reference(15).extension(1000)

        # Hexadecimal
        >>> hex(tag)
        '0x3218013480001e00000003e8'

        # Binary
        >>> bin(tag)
        '0b1100100001100000000001001101001000000000000000000111100000000000000000000000000000001111101000'


Constants
^^^^^^^^^

Filters

.. data:: SGLN.FILTER_ALL

.. data:: SGLN.FILTER_RESERVED_*

    Replace asterisk with 1-7.

Sizes

.. data:: SGLN.SIZE_96

    96 bit tag size.

.. data:: SGLN.SIZE_195

    195 bit tag size.

Headers

.. data:: SGLN.HEADER_BARCODE

    GS1 specified barcode header: ``414``.

.. data:: SGLN.HEADER_96

    GS1 specified hexadecimal header for 96 bit SGLN tags: ``0x32``.

.. data:: SGLN.HEADER_195

    GS1 specified hexadecimal header for 202 bit SGLN tags: ``0x39``.


.. data:: SGLN.SGLN_96

    Human readable GS1 specified header for 96 bit SGLN tags: ``sgln-96``.


.. data:: SGLN.SGLN_195

    Human readable GS1 specified header for 202 bit SGLN tags: ``sgln-195``.


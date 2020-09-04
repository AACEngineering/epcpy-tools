GIAI
----

.. autoclass:: epc.schemes.GIAI
    
    .. automethod:: filter

    .. automethod:: company_prefix

    .. automethod:: asset_reference

    .. method:: tag_size

        Set the size for the tag.

        :param tag_size: Tag size in bits. Defaults to ``SIZE_96``.
        :type tag_size: int

        :raises AttributeError: Invalid tag size specified.

        :return: The GIAI tag object.
        :rtype: :class:`epc.schemes.GIAI`

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

        >>> tag = GIAI()
        >>> tag.company_prefix('00200').asset_reference(50)

        # Hexadecimal
        >>> hex(tag)
        '0x341800320000000000000032'

        # Binary
        >>> bin(tag)
        '0b1101000001100000000000001100100000000000000000000000000000000000000000000000000000000000110010'


Constants
^^^^^^^^^

Filters

.. data:: GIAI.FILTER_ALL

.. data:: GIAI.FILTER_RAIL

.. data:: GIAI.FILTER_RESERVED_*

    Replace asterisk with 2-7.

Sizes

.. data:: GIAI.SIZE_96

    96 bit tag size.

.. data:: GIAI.SIZE_202

    202 bit tag size. Supports alphanumeric characters for the asset reference.

Headers

.. data:: GIAI.HEADER_BARCODE

    GS1 specified barcode header: ``8004``.

.. data:: GIAI.HEADER_96

    GS1 specified hexadecimal header for 96 bit GID tags: ``0x34``.

.. data:: GIAI.HEADER_202

    GS1 specified hexadecimal header for 202 bit GID tags: ``0x38``.


.. data:: GIAI.GID_96

    Human readable GS1 specified header for 96 bit GID tags: ``giai-96``.


.. data:: GIAI.GID_202

    Human readable GS1 specified header for 202 bit GID tags: ``giai-202``.


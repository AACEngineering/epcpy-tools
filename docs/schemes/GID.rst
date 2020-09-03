GID
---

.. autoclass:: epc.schemes.GID

    .. automethod:: manager_number

    .. automethod:: object_class

    .. automethod:: serial_number

    .. autoproperty:: tag_uri

    .. autoproperty:: pure_identity_uri

    .. autoproperty:: values

    .. automethod:: decode_epc

    .. automethod:: check_fields


.. hint::

    To get the encoded tag data, use python's built in conversion methods:

    .. code-block:: python
        :emphasize-lines: 5, 9

        >>> tag = GID()
        >>> tag.manager_number(31231).object_class(11).serial_number(12)

        # Hexadecimal
        >>> hex(tag)
        '0x3500079ff00000b00000000c'

        # Binary
        >>> bin(tag)
        '0b1101010000000000000111100111111111000000000000000000001011000000000000000000000000000000001100'


Constants
^^^^^^^^^

.. data:: GID.SIZE_96

    96 bit tag size. Only size supported for this scheme.

.. data:: GID.HEADER_96

    GS1 specified hexadecimal header for 96 bit GID tags: ``0x35``.

.. data:: GID.GID_96

    Human readable GS1 specified header for 96 bit GID tags: ``gid-96``.

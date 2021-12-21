.. _examples:

Examples
========


General
-------

Decode an EPC with unknown encoding

.. code-block:: python

    >>> from epc.utils import decode_epc
    >>> decode_epc('341401388000000000000001')  # '0x' prefix is optional
    <epc.schemes.GIAI urn:epc:id:giai:0020000.1>


Decode a barcode

.. code-block:: python

    >>> from epc.utils.barcode import decode_barcode
    >>> decode_barcode('8003000000100000141', company_prefix_length=6)
    <epc.schemes.GRAI urn:epc:id:grai:000001.000001.1>


.. tip::

    The `company_prefix_length` field is the number of digits in the expected `GS1 Company Prefix <https://www.gs1.org/standards/id-keys/company-prefix>`_.


Convert an EPC to barcode (for schemes that support barcodes)

.. code-block:: python

    >>> from epc.utils import decode_epc
    >>> decode_epc('341401388000000000000001').barcode
    '800400200001'


GID Tags
--------

:class:`epc.schemes.GID`

.. code-block:: python

    >>> from epc.schemes import GID

    # Create an uninitialized tag object
    >>> my_tag = GID()

    # Assign the required tag attributes
    >>> my_tag.manager_number(951001).object_class(15).serial_number(1)
    <epc.schemes.GID urn:epc:id:gid:951001.15.1>

    # Get the encoded tag data
    >>> hex(my_tag)
    '0x3500e82d900000f000000001'

    >>> my_tag.pure_identity_uri
    'urn:epc:tag:gid-96:951001.15.1'

    # Strings will be automatically converted to integers
    >>> my_tag.serial_number('90')
    <epc.schemes.GID urn:epc:id:gid:951001.15.90>

    # Initialize a new tag from tag data
    >>> GID(epc='0x3500e82d900000f000000001')
    <epc.schemes.GID urn:epc:id:gid:951001.15.1>


GIAI Tags
---------

:class:`epc.schemes.GIAI`

.. code-block:: python

    >>> from epc.schemes import GIAI

    >>> my_tag = GIAI()

    # Initialize tag
    >>> my_tag.company_prefix('000200').asset_reference(50)
    <epc.schemes.GIAI urn:epc:id:giai:000200.50>

    # Set tag size to 202 bit
    >>> my_tag.tag_size(GIAI.SIZE_202)
    >>> my_tag.asset_reference('HIPPO')
    <epc.schemes.GIAI urn:epc:id:giai:000200.HIPPO>

    # Get the barcode
    >>> my_tag.barcode
    '8004000200HIPPO'

    >>> my_tag.barcode_humanized
    '(8004) 000200 HIPPO'

    # Set a tag filter
    >>> my_tag.filter(GIAI.FILTER_RAIL)


GRAI Tags
---------

:class:`epc.schemes.GIAI`

.. code-block:: python

    >>> from epc.schemes import GRAI

    >>> my_tag = GRAI().tag_size(GRAI.SIZE_170)

    >>> my_tag.company_prefix('000123').asset_type(8).serial_number('WOW!')
    <epc.schemes.GRAI urn:epc:id:grai:000123.000008.WOW!>

    # Get tag URI
    >>> my_tag.tag_uri
    'urn:epc:tag:grai-170:0.000123.000008.WOW!'

    # Barcode
    >>> my_tag.barcode
    '800300001230000082WOW!'


SGLN Tags
---------

:class:`epc.schemes.SGLN`

.. code-block:: python

    >>> from epc.schemes import SGLN

    >>> my_tag = SGLN()

    >>> my_tag.company_prefix('001234').location_reference(15).extension(1000)
    <epc.schemes.SGLN urn:epc:id:sgln:001234.000015.1000>


SGTIN Tags
----------

:class:`epc.schemes.SGTIN`

.. code-block:: python

    >>> from epc.schemes import SGTIN

    >>> my_tag = SGTIN()

    >>> my_tag.company_prefix('001234').item_reference(15).serial_number(1000)
    <epc.schemes.SGTIN urn:epc:id:sgtin:001234.0000015.1000>

    # Create a tag from a GTIN
    >>> my_tag = SGTIN()
    >>> my_tag.decode_gtin('80614141123458', company_prefix_length=7, serial_number=6789)
    >>> my_tag.tag_uri
    'urn:epc:tag:sgtin-96:0.0614141.812345.6789'

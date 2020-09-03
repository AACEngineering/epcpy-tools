Getting Started
===============


Installation requirements:

* Python 3.5 or above


To install::

    pip install epc-encoding-utils


Examples:

.. code-block:: python
    :caption: Create a GID tag

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

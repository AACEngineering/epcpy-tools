EPC Encoding Utils
------------------

[![Documentation Status](https://readthedocs.org/projects/epcpy-tools/badge/?version=latest)](https://epcpy-tools.readthedocs.io/en/latest/?badge=latest)
[![](https://img.shields.io/pypi/v/epc-encoding-utils.svg)](https://pypi.org/project/epc-encoding-utils/)

```
pip install epc-encoding-utils
```

Library for encoding/decoding and representing GS1 Electronic Product Codes (EPCs). It supports the following encoding schemes:

- GIAI
- GID
- GRAI
- SGLN

The library's goal is to abstract away much of the complexity of converting between tag representations, and make generating tags and barcodes simple.


## Docs

https://epcpy-tools.readthedocs.io/en/latest/index.html


### Examples

Create a new GID encoded tag

```python
>>> from epc.schemes import GID
>>> tag = GID()
>>> tag.manager_number(31231).object_class(11).serial_number(12)
<epc.schemes.GID urn:epc:id:gid:31231.11.12>

>>> hex(tag)
'0x3500079ff00000b00000000c'

>>> tag.tag_uri
'urn:epc:tag:gid-96:31231.11.12'
```

Generate GIAI barcode from/to a hexadecimal tag data representation

```python
>>> from epc.schemes import GIAI
>>> tag = GIAI(epc='0x341401388000000000000001')
>>> tag.barcode
'800400200001'

>>> tag.barcode_humanized
'(8004) 0020000 1'

>>> tag = GIAI(barcode='800400200001', company_prefix_length=7)
>>> hex(tag)
'0x341401388000000000000001'
```

Decode an EPC data tag with unknown encoding

```python
>>> from epc.utils import decode_epc
>>> tag = decode_epc('341401388000000000000001')  # '0x' prefix is optional
>>> print(tag)
<epc.schemes.GIAI urn:epc:id:giai:0020000.1>
```

This library was built based on the Tag Data Standard v1.11.


### Running Tests

```shell
python -m unittest discover -s epc/schemes/tests
```

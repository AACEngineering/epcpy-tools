Changelog
---------

### v1.4

- Fixed `decode_barcode()` not correctly detecting SGLN encodings.


### v1.3

- SGTIN-96: Allow serial numbers with the value of 0.


### v1.2

- Added SGTIN encoding support.
- Fixed sgln-195 encoding not being correctly detected when using `decode_epc()`.


### v1.1

- Fixed incorrect SGLN check digit calculation if the sum of digits was a multiple of 10. Thanks @endreszabo!


### v1.0

- Initial release.

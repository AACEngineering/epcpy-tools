from unittest import TestCase

from epc.schemes import SGLN


class SGLNTest(TestCase):
    def test_96_encode(self):
        """Test SGLN-96 encoding"""
        epc = SGLN().tag_size(SGLN.SIZE_96).filter(SGLN.FILTER_ALL)
        epc.company_prefix(1, 6).location_reference(1).extension(0)

        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:000001.000001.0')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-96:0.000001.000001.0')
        self.assertEqual(hex(epc), '0x321800004000020000000000')

        epc.company_prefix('0020000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:0020000.00001.0')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-96:0.0020000.00001.0')
        self.assertEqual(hex(epc), '0x321401388000020000000000')

        epc.company_prefix(320000000000, 12)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:320000000000..0')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-96:0.320000000000..0')
        self.assertEqual(hex(epc), '0x32012a05f200000000000000')

        epc.company_prefix('0123456').location_reference(5000).extension(1234)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:0123456.05000.1234')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-96:0.0123456.05000.1234')
        self.assertEqual(hex(epc), '0x3214078900271000000004d2')

    def test_96_decode(self):
        """Test SGLN-96 decoding"""
        epc = SGLN(epc='32157bb91483971f35d00d06')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:6221381.16843.1233558441222')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-96:0.6221381.16843.1233558441222')

        epc = SGLN(epc='3274257bf46072000000162e')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:0614141.12345.5678')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-96:3.0614141.12345.5678')

        # NOTE:
        # On the next two EPCs, the company_prefix length is 12, which limits the location
        # reference to a single bit.

        # location_reference_bit set to 1
        # The GS1 online decoder will give an error (location reference value out of range),
        # however our implementation will accept this.
        epc = SGLN(epc='3262fe9fe27ae2cef646e093')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:823156842168..888895103123')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-96:3.823156842168..888895103123')

        # location reference bit set to 0
        epc = SGLN(epc='3262fe9fe27ae0cef646e093')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:823156842168..888895103123')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-96:3.823156842168..888895103123')

    def test_195_encode(self):
        """Test SGLN-195 encoding"""
        epc = SGLN().tag_size(SGLN.SIZE_195).filter(SGLN.FILTER_ALL)
        epc.company_prefix(1, 6).location_reference(1).extension(1)

        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:000001.000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-195:0.000001.000001.1')
        self.assertEqual(hex(epc), '0x39180000400002c4000000000000000000000000000000000000')

        epc.company_prefix('0020000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:0020000.00001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-195:0.0020000.00001.1')
        self.assertEqual(hex(epc), '0x39140138800002c4000000000000000000000000000000000000')

        epc.company_prefix(320000000000, 12)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:320000000000..1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-195:0.320000000000..1')
        self.assertEqual(hex(epc), '0x39012a05f20000c4000000000000000000000000000000000000')

        # Test character encoding
        epc.company_prefix('12345678').extension('ABCDEFGHIJKLMNOPQRST')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:sgln:12345678.0001.ABCDEFGHIJKLMNOPQRST'
        )
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-195:0.12345678.0001.ABCDEFGHIJKLMNOPQRST')
        self.assertEqual(hex(epc), '0x39105e30a70003061438916347912654b993674fa146953a8000')

        epc.company_prefix(1, 6).extension('!"%&\'()*+,-./012')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:sgln:000001.000001.!%22%25%26\'()*+,-.%2F012'
        )
        self.assertEqual(
            epc.tag_uri, 'urn:epc:tag:sgln-195:0.000001.000001.!%22%25%26\'()*+,-.%2F012'
        )
        self.assertEqual(hex(epc), '0x39180000400002851254c9d42954ad62d5cbd831640000000000')

    def test_195_decode(self):
        """Test SGLN-195 decoding"""
        epc = SGLN(epc='39180000400002c4000000000000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:000001.000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-195:0.000001.000001.1')

        epc = SGLN(epc='39140138800002c4000000000000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:0020000.00001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-195:0.0020000.00001.1')

        epc = SGLN(epc='39012a05f20000c4000000000000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgln:320000000000..1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-195:0.320000000000..1')

        # Test character decoding
        epc = SGLN(epc='39105e30a70003061438916347912654b993674fa146953a8000')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:sgln:12345678.0001.ABCDEFGHIJKLMNOPQRST'
        )
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgln-195:0.12345678.0001.ABCDEFGHIJKLMNOPQRST')

        epc = SGLN(epc='39180000400002851254c9d42954ad62d5cbd831640000000000')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:sgln:000001.000001.!%22%25%26\'()*+,-.%2F012'
        )
        self.assertEqual(
            epc.tag_uri, 'urn:epc:tag:sgln-195:0.000001.000001.!%22%25%26\'()*+,-.%2F012'
        )

    def test_barcode_encode(self):
        """Test SGLN barcode encoding"""
        epc = SGLN(epc='32157bb91483971f35d00d06')
        self.assertEqual(epc.barcode, '41462213811684392541233558441222')
        self.assertEqual(epc.barcode_humanized, '(414)6221381168439(254)1233558441222')

        epc = SGLN(epc='3274257bf46072000000162e')
        self.assertEqual(epc.barcode, '41406141411234522545678')
        self.assertEqual(epc.barcode_humanized, '(414)0614141123452(254)5678')

        epc = SGLN(epc='39140138800002c4000000000000000000000000000000000000')
        self.assertEqual(epc.barcode, '41400200000000152541')
        self.assertEqual(epc.barcode_humanized, '(414)0020000000015(254)1')

        epc = SGLN(epc='39180000400002851254c9d42954ad62d5cbd831640000000000')
        self.assertEqual(epc.barcode, '4140000010000014254!"%&\'()*+,-./012')
        self.assertEqual(epc.barcode_humanized, '(414)0000010000014(254)!"%&\'()*+,-./012')

    def test_barcode_decode(self):
        """Test SGLN barcode decoding"""
        epc = SGLN(barcode='41462213811684392541233558441222', company_prefix_length=7)
        self.assertEqual(hex(epc), '0x32157bb91483971f35d00d06')

        epc = SGLN(barcode='41432000000000012540', company_prefix_length=12)
        self.assertEqual(hex(epc), '0x32012a05f200000000000000')

        epc = SGLN(barcode='4140020000000015254A', company_prefix_length=7)
        self.assertEqual(hex(epc), '0x3914013880000304000000000000000000000000000000000000')

        epc = SGLN(barcode='4140000010000014254!"%&\'()*+,-./012', company_prefix_length=6)
        self.assertEqual(hex(epc), '0x39180000400002851254c9d42954ad62d5cbd831640000000000')

    def test_check_digit(self):
        """Test SGLN Check Digit Calcuation"""
        epc = SGLN().company_prefix('2488320').location_reference(22830).extension(0)
        self.assertEqual(epc.calc_check_digit(), 0)

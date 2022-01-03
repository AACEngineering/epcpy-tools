from unittest import TestCase

from epc.schemes import SGTIN


class SGTINTest(TestCase):
    def test_96_encode(self):
        """Test SGTIN-96 encoding"""
        epc = SGTIN().tag_size(SGTIN.SIZE_96).filter(SGTIN.FILTER_ALL)
        epc.company_prefix(1, 6).item_reference(1).serial_number(1)

        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:000001.0000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.000001.0000001.1')
        self.assertEqual(epc.gtin, '00000010000014')
        self.assertEqual(hex(epc), '0x301800004000004000000001')

        epc.company_prefix('0020000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:0020000.000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.0020000.000001.1')
        self.assertEqual(epc.gtin, '00020000000015')
        self.assertEqual(hex(epc), '0x301401388000004000000001')

        epc.company_prefix(320000000000, 12)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:320000000000.1.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.320000000000.1.1')
        self.assertEqual(epc.gtin, '13200000000008')
        self.assertEqual(hex(epc), '0x30012a05f200004000000001')

        epc.serial_number(0)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:320000000000.1.0')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.320000000000.1.0')
        self.assertEqual(epc.gtin, '13200000000008')
        self.assertEqual(hex(epc), '0x30012a05f200004000000000')

        epc.company_prefix('32000000').item_reference('25000').serial_number(51681623)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:32000000.25000.51681623')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.32000000.25000.51681623')
        self.assertEqual(epc.gtin, '23200000050000')
        self.assertEqual(hex(epc), '0x3010f42400186a0003149957')

    def test_96_decode(self):
        """Test SGTIN-96 decoding"""
        epc = SGTIN(epc='301800004000004000000001')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:000001.0000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.000001.0000001.1')
        self.assertEqual(epc.gtin, '00000010000014')

        epc = SGTIN(epc='301401388000004000000001')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:0020000.000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.0020000.000001.1')
        self.assertEqual(epc.gtin, '00020000000015')

        epc = SGTIN(epc='30012a05f200004000000001')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:320000000000.1.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.320000000000.1.1')
        self.assertEqual(epc.gtin, '13200000000008')

        epc = SGTIN(epc='0x30012a05f200004000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:320000000000.1.0')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.320000000000.1.0')
        self.assertEqual(epc.gtin, '13200000000008')

        epc = SGTIN(epc='3010f42400186a0003149957')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:32000000.25000.51681623')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.32000000.25000.51681623')
        self.assertEqual(epc.gtin, '23200000050000')

    def test_198_encode(self):
        """Test SGTIN-198 encoding"""
        epc = SGTIN().tag_size(SGTIN.SIZE_198).filter(SGTIN.FILTER_ALL)
        epc.company_prefix(1, 6).item_reference(1).serial_number(1)

        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:000001.0000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-198:0.000001.0000001.1')
        self.assertEqual(epc.gtin, '00000010000014')
        self.assertEqual(hex(epc), '0x3618000040000058800000000000000000000000000000000000')

        epc.company_prefix('0020000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:0020000.000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-198:0.0020000.000001.1')
        self.assertEqual(epc.gtin, '00020000000015')
        self.assertEqual(hex(epc), '0x3614013880000058800000000000000000000000000000000000')

        epc.company_prefix(320000000000, 12)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:320000000000.1.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-198:0.320000000000.1.1')
        self.assertEqual(epc.gtin, '13200000000008')
        self.assertEqual(hex(epc), '0x36012a05f2000058800000000000000000000000000000000000')

        # Test character encoding
        epc.company_prefix(1, 6).serial_number('!"%&\'()*+,-./012')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:sgtin:000001.0000001.!%22%25%26\'()*+,-.%2F012'
        )
        self.assertEqual(
            epc.tag_uri, 'urn:epc:tag:sgtin-198:0.000001.0000001.!%22%25%26\'()*+,-.%2F012'
        )
        self.assertEqual(epc.gtin, '00000010000014')
        self.assertEqual(hex(epc), '0x3618000040000050a24a993a852a95ac5ab97b062c8000000000')

    def test_198_decode(self):
        """Test SGTIN-198 decoding"""
        epc = SGTIN(epc='3618000040000058800000000000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:000001.0000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-198:0.000001.0000001.1')
        self.assertEqual(epc.gtin, '00000010000014')

        epc = SGTIN(epc='3614013880000058800000000000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:0020000.000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-198:0.0020000.000001.1')
        self.assertEqual(epc.gtin, '00020000000015')

        epc = SGTIN(epc='36012a05f2000058800000000000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:320000000000.1.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-198:0.320000000000.1.1')
        self.assertEqual(epc.gtin, '13200000000008')

        # Test character decoding
        epc = SGTIN(epc='3618000040000050a24a993a852a95ac5ab97b062c8000000000')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:sgtin:000001.0000001.!%22%25%26\'()*+,-.%2F012'
        )
        self.assertEqual(
            epc.tag_uri, 'urn:epc:tag:sgtin-198:0.000001.0000001.!%22%25%26\'()*+,-.%2F012'
        )
        self.assertEqual(epc.gtin, '00000010000014')

    def test_barcode_encode(self):
        """Test SGTIN barcode encoding"""
        epc = SGTIN(epc='3074257bf4cf5e4fcf27c6ff')
        self.assertEqual(epc.barcode, '01206141411234562167899999999')
        self.assertEqual(epc.barcode_humanized, '(01) 20614141123456 (21) 67899999999')

        epc = SGTIN(epc='301401388000004000000001')
        self.assertEqual(epc.barcode, '0100020000000015211')
        self.assertEqual(epc.barcode_humanized, '(01) 00020000000015 (21) 1')

        epc = SGTIN(epc='36012a05f2000058800000000000000000000000000000000000')
        self.assertEqual(epc.barcode, '0113200000000008211')
        self.assertEqual(epc.barcode_humanized, '(01) 13200000000008 (21) 1')

        epc = SGTIN(epc='0x3618000040000050a24a993a852a95ac5ab97b062c8000000000')
        self.assertEqual(epc.barcode, '010000001000001421!"%&\'()*+,-./012')
        self.assertEqual(epc.barcode_humanized, '(01) 00000010000014 (21) !"%&\'()*+,-./012')

    def test_barcode_decode(self):
        """Test SGTIN barcode decoding"""
        epc = SGTIN(barcode='0120614141123456216789999999', company_prefix_length=7)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:0614141.212345.6789999999')
        self.assertEqual(hex(epc), '0x3014257bf4cf5e4194b72d7f')

        epc = SGTIN(barcode='0100020000000015211', company_prefix_length=7)
        self.assertEqual(hex(epc), '0x301401388000004000000001')

        epc = SGTIN(barcode='011320000000000821A', company_prefix_length=12)
        self.assertEqual(hex(epc), '0x36012a05f2000060800000000000000000000000000000000000')

        epc = SGTIN(barcode='010000001000001421!"%&\'()*+,-./012', company_prefix_length=6)
        self.assertEqual(hex(epc), '0x3618000040000050a24a993a852a95ac5ab97b062c8000000000')

    def test_gtin_encode(self):
        """Test SGTIN encode from GTIN"""
        epc = SGTIN()

        epc.decode_gtin('00000010000014', company_prefix_length=6, serial_number='1')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:000001.0000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.000001.0000001.1')
        self.assertEqual(hex(epc), '0x301800004000004000000001')

        epc.decode_gtin('13200000000008', company_prefix_length=12, serial_number='1')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:320000000000.1.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.320000000000.1.1')
        self.assertEqual(hex(epc), '0x30012a05f200004000000001')

        epc.decode_gtin('23200000050000', company_prefix_length=8, serial_number='51681623')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:sgtin:32000000.25000.51681623')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:sgtin-96:0.32000000.25000.51681623')
        self.assertEqual(hex(epc), '0x3010f42400186a0003149957')

        # GTIN-13
        epc.decode_gtin('0000010000014', company_prefix_length=6, serial_number='!"%&\'()*+,-./012')
        self.assertEqual(epc.pure_identity_uri,
                         'urn:epc:id:sgtin:000001.0000001.!%22%25%26\'()*+,-.%2F012')
        self.assertEqual(epc.tag_uri,
                         'urn:epc:tag:sgtin-198:0.000001.0000001.!%22%25%26\'()*+,-.%2F012')
        self.assertEqual(hex(epc), '0x3618000040000050a24a993a852a95ac5ab97b062c8000000000')

        # GTIN-12
        epc.decode_gtin('000010000014', company_prefix_length=6, serial_number='!"%&\'()*+,-./012')
        self.assertEqual(epc.pure_identity_uri,
                         'urn:epc:id:sgtin:000001.0000001.!%22%25%26\'()*+,-.%2F012')
        self.assertEqual(epc.tag_uri,
                         'urn:epc:tag:sgtin-198:0.000001.0000001.!%22%25%26\'()*+,-.%2F012')
        self.assertEqual(hex(epc), '0x3618000040000050a24a993a852a95ac5ab97b062c8000000000')

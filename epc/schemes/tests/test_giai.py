from unittest import TestCase

from epc.schemes import GIAI


class GIAITest(TestCase):
    def test_96_encode(self):
        """Test GIAI-96 encoding"""
        epc = GIAI().tag_size(GIAI.SIZE_96).filter(GIAI.FILTER_ALL)
        epc.company_prefix(1, 6)
        epc.asset_reference(1)

        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-96:0.000001.1')
        self.assertEqual(hex(epc), '0x341800004000000000000001')

        epc.company_prefix('0020000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:0020000.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-96:0.0020000.1')
        self.assertEqual(hex(epc), '0x341401388000000000000001')

        epc.company_prefix(320000000000, 12)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:320000000000.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-96:0.320000000000.1')
        self.assertEqual(hex(epc), '0x34012a05f200000000000001')

    def test_96_decode(self):
        """Test GIAI-96 decoding"""
        epc = GIAI(epc='341800004000000000000001')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-96:0.000001.1')

        epc = GIAI(epc='341401388000000000000001')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:0020000.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-96:0.0020000.1')

        epc = GIAI(epc='34012a05f200000000000001')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:320000000000.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-96:0.320000000000.1')

    def test_202_encode(self):
        """Test GIAI-202 encoding"""
        epc = GIAI().tag_size(GIAI.SIZE_202).filter(GIAI.FILTER_ALL)
        epc.company_prefix(1, 6).asset_reference(1)

        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-202:0.000001.1')
        self.assertEqual(hex(epc), '0x3818000058800000000000000000000000000000000000000000')

        epc.company_prefix('0020000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:0020000.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-202:0.0020000.1')
        self.assertEqual(hex(epc), '0x3814013881880000000000000000000000000000000000000000')

        epc.company_prefix(320000000000, 12)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:320000000000.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-202:0.320000000000.1')
        self.assertEqual(hex(epc), '0x38012a05f2000188000000000000000000000000000000000000')

        # Test character encoding
        epc.company_prefix(1, 6).asset_reference('!"%&\'()*+,-./0123456789:')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:giai:000001.!%22%25%26\'()*+,-.%2F0123456789:'
        )
        self.assertEqual(
            epc.tag_uri, 'urn:epc:tag:giai-202:0.000001.!%22%25%26\'()*+,-.%2F0123456789:'
        )
        self.assertEqual(hex(epc), '0x3818000050a24a993a852a95ac5ab97b062c99b46ad9bb872e80')

        epc.asset_reference(';<=>?ABCDEFGHIJKLMNOPQRS')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:giai:000001.;%3C=%3E%3FABCDEFGHIJKLMNOPQRS'
        )
        self.assertEqual(
            epc.tag_uri, 'urn:epc:tag:giai-202:0.000001.;%3C=%3E%3FABCDEFGHIJKLMNOPQRS'
        )
        self.assertEqual(hex(epc), '0x381800005dbc7af9fc1850e2458d1e449952e64d9d3e851a54c0')

        epc.asset_reference('STUVWXYZ_abcdefghijklmno')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:000001.STUVWXYZ_abcdefghijklmno')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-202:0.000001.STUVWXYZ_abcdefghijklmno')
        self.assertEqual(hex(epc), '0x3818000069d4ab5abd8b36afe1c58f265cd9f469d5af66dddbc0')

        epc.asset_reference('pqrstuvwxyz')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:000001.pqrstuvwxyz')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-202:0.000001.pqrstuvwxyz')
        self.assertEqual(hex(epc), '0x381800007871e5cfa75eddfc79f4000000000000000000000000')

    def test_202_decode(self):
        """Test GIAI-202 decoding"""
        epc = GIAI(epc='3818000058800000000000000000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-202:0.000001.1')

        epc = GIAI(epc='3814013881880000000000000000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:0020000.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-202:0.0020000.1')

        epc = GIAI(epc='38012a05f2000188000000000000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:320000000000.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-202:0.320000000000.1')

        # Test character encoding
        epc = GIAI(epc='3818000050a24a993a852a95ac5ab97b062c99b46ad9bb872e80')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:giai:000001.!%22%25%26\'()*+,-.%2F0123456789:'
        )
        self.assertEqual(
            epc.tag_uri, 'urn:epc:tag:giai-202:0.000001.!%22%25%26\'()*+,-.%2F0123456789:'
        )

        epc = GIAI(epc='381800005dbc7af9fc1850e2458d1e449952e64d9d3e851a54c0')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:giai:000001.;%3C=%3E%3FABCDEFGHIJKLMNOPQRS'
        )
        self.assertEqual(
            epc.tag_uri, 'urn:epc:tag:giai-202:0.000001.;%3C=%3E%3FABCDEFGHIJKLMNOPQRS'
        )

        epc = GIAI(epc='3818000069d4ab5abd8b36afe1c58f265cd9f469d5af66dddbc0')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:000001.STUVWXYZ_abcdefghijklmno')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-202:0.000001.STUVWXYZ_abcdefghijklmno')

        epc = GIAI(epc='381800007871e5cfa75eddfc79f4000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:giai:000001.pqrstuvwxyz')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:giai-202:0.000001.pqrstuvwxyz')

    def test_barcode_encode(self):
        """Test GIAI barcode encoding"""
        epc = GIAI(epc='341800004000000000000001')
        self.assertEqual(epc.barcode, '80040000011')
        self.assertEqual(epc.barcode_humanized, '(8004) 000001 1')

        epc = GIAI(epc='38012a05f2000188000000000000000000000000000000000000')
        self.assertEqual(epc.barcode, '80043200000000001')
        self.assertEqual(epc.barcode_humanized, '(8004) 320000000000 1')

        epc = GIAI(epc='3818000050a24a993a852a95ac5ab97b062c99b46ad9bb872e80')
        self.assertEqual(epc.barcode, '8004000001!"%&\'()*+,-./0123456789:')
        self.assertEqual(epc.barcode_humanized, '(8004) 000001 !"%&\'()*+,-./0123456789:')

    def test_barcode_decode(self):
        """Test GIAI barcode decoding"""
        epc = GIAI(barcode='80040000011', company_prefix_length=6)
        self.assertEqual(hex(epc), '0x341800004000000000000001')

        epc = GIAI(barcode='80043200000000001', company_prefix_length=12)
        self.assertEqual(hex(epc), '0x34012a05f200000000000001')

        epc = GIAI(barcode='8004000001!"%&\'()*+,-./0123456789:', company_prefix_length=6)
        self.assertEqual(hex(epc), '0x3818000050a24a993a852a95ac5ab97b062c99b46ad9bb872e80')

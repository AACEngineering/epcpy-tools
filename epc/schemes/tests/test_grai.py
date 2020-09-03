from unittest import TestCase

from epc.schemes import GRAI


class GRAITest(TestCase):
    def test_96_encode(self):
        """Test GRAI-96 encoding"""
        epc = GRAI().tag_size(GRAI.SIZE_96).filter(GRAI.FILTER_ALL)
        epc.company_prefix(1, 6).asset_type(1).serial_number(1)

        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:000001.000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-96:0.000001.000001.1')
        self.assertEqual(hex(epc), '0x331800004000004000000001')

        epc.company_prefix('0020000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:0020000.00001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-96:0.0020000.00001.1')
        self.assertEqual(hex(epc), '0x331401388000004000000001')

        epc.company_prefix(320000000000, 12)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:320000000000..1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-96:0.320000000000..1')
        self.assertEqual(hex(epc), '0x33012a05f200000000000001')

    def test_96_decode(self):
        """Test GRAI-96 decoding"""
        epc = GRAI(epc='331800004000004000000001')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:000001.000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-96:0.000001.000001.1')

        epc = GRAI(epc='331401388000004000000001')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:0020000.00001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-96:0.0020000.00001.1')

        epc = GRAI(epc='33012a05f200000000000001')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:320000000000..1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-96:0.320000000000..1')

    def test_170_encode(self):
        """Test GIAI-170 encoding"""
        epc = GRAI().tag_size(GRAI.SIZE_170).filter(GRAI.FILTER_ALL)
        epc.company_prefix(1, 6).asset_type(1).serial_number(1)

        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:000001.000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-170:0.000001.000001.1')
        self.assertEqual(hex(epc), '0x37180000400000588000000000000000000000000000')

        epc.company_prefix('0020000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:0020000.00001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-170:0.0020000.00001.1')
        self.assertEqual(hex(epc), '0x37140138800000588000000000000000000000000000')

        epc.company_prefix(320000000000, 12)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:320000000000..1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-170:0.320000000000..1')
        self.assertEqual(hex(epc), '0x37012a05f20000188000000000000000000000000000')

        # Test character encoding
        epc.company_prefix(1, 6).serial_number('!"%&\'()*+,-./012')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:grai:000001.000001.!%22%25%26\'()*+,-.%2F012'
        )
        self.assertEqual(
            epc.tag_uri, 'urn:epc:tag:grai-170:0.000001.000001.!%22%25%26\'()*+,-.%2F012'
        )
        self.assertEqual(hex(epc), '0x3718000040000050a24a993a852a95ac5ab97b062c80')

    def test_170_decode(self):
        """Test GRAI-170 decoding"""
        epc = GRAI(epc='37180000400000588000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:000001.000001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-170:0.000001.000001.1')

        epc = GRAI(epc='37140138800000588000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:0020000.00001.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-170:0.0020000.00001.1')

        epc = GRAI(epc='37012a05f20000188000000000000000000000000000')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:grai:320000000000..1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:grai-170:0.320000000000..1')

        # Test character decoding
        epc = GRAI(epc='3718000040000050a24a993a852a95ac5ab97b062c80')
        self.assertEqual(
            epc.pure_identity_uri, 'urn:epc:id:grai:000001.000001.!%22%25%26\'()*+,-.%2F012'
        )
        self.assertEqual(
            epc.tag_uri, 'urn:epc:tag:grai-170:0.000001.000001.!%22%25%26\'()*+,-.%2F012'
        )

    def test_barcode_encode(self):
        """Test GRAI barcode encoding"""
        epc = GRAI(epc='331800004000004000000001')
        self.assertEqual(epc.barcode, '8003000000100000141')
        self.assertEqual(epc.barcode_humanized, '(8003) 0 000001 000001 4 1')

        epc = GRAI(epc='33012a05f200000000000001')
        self.assertEqual(epc.barcode, '8003032000000000011')
        self.assertEqual(epc.barcode_humanized, '(8003) 0 320000000000 1 1')

        epc = GRAI(epc='37140138800000588000000000000000000000000000')
        self.assertEqual(epc.barcode, '8003000200000000151')
        self.assertEqual(epc.barcode_humanized, '(8003) 0 0020000 00001 5 1')

        epc = GRAI(epc='3718000040000050a24a993a852a95ac5ab97b062c80')
        self.assertEqual(epc.barcode, '800300000010000014!"%&\'()*+,-./012')
        self.assertEqual(epc.barcode_humanized, '(8003) 0 000001 000001 4 !"%&\'()*+,-./012')

    def test_barcode_decode(self):
        """Test GRAI barcode decoding"""
        epc = GRAI(barcode='8003000000100000141', company_prefix_length=6)
        self.assertEqual(hex(epc), '0x331800004000004000000001')

        epc = GRAI(barcode='8003032000000000011', company_prefix_length=12)
        self.assertEqual(hex(epc), '0x33012a05f200000000000001')

        epc = GRAI(barcode='8003000200000000151', company_prefix_length=7)
        self.assertEqual(hex(epc), '0x331401388000004000000001')

        epc = GRAI(barcode='800300000010000014!"%&\'()*+,-./012', company_prefix_length=6)
        self.assertEqual(hex(epc), '0x3718000040000050a24a993a852a95ac5ab97b062c80')

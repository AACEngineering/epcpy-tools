from unittest import TestCase

from epc.schemes import GID


class GIDTest(TestCase):
    def test_96_encode(self):
        """Test GID-96 encoding"""
        epc = GID().tag_size(GID.SIZE_96)
        epc.manager_number(1).object_class(1).serial_number(1)

        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:gid:1.1.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:gid-96:1.1.1')
        self.assertEqual(hex(epc), '0x350000001000001000000001')

        epc.manager_number(20000).object_class(50).serial_number(9999)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:gid:20000.50.9999')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:gid-96:20000.50.9999')
        self.assertEqual(hex(epc), '0x350004e2000003200000270f')

        epc.manager_number(268435455).object_class(16777215).serial_number(68719476735)
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:gid:268435455.16777215.68719476735')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:gid-96:268435455.16777215.68719476735')
        self.assertEqual(hex(epc), '0x35ffffffffffffffffffffff')

    def test_96_decode(self):
        """Test GID-96 decoding"""
        epc = GID(epc='350000001000001000000001')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:gid:1.1.1')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:gid-96:1.1.1')

        epc = GID(epc='350004e2000003200000270f')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:gid:20000.50.9999')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:gid-96:20000.50.9999')

        epc = GID(epc='35ffffffffffffffffffffff')
        self.assertEqual(epc.pure_identity_uri, 'urn:epc:id:gid:268435455.16777215.68719476735')
        self.assertEqual(epc.tag_uri, 'urn:epc:tag:gid-96:268435455.16777215.68719476735')

#!/usr/bin/env python

# Copyright 2019, The Android Open Source Project
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Unit tests for aftltool."""

# pylint: disable=unused-import
from __future__ import print_function

import binascii
import io
import os
import sys
import unittest

import aftltool
import avbtool
import proto.aftl_pb2
import proto.api_pb2
import proto.trillian_pb2


class AftltoolTestCase(unittest.TestCase):

  def setUp(self):
    """Sets up the test bed for the unit tests."""
    super(AftltoolTestCase, self).setUp()

    # Redirects the stderr to /dev/null when running the unittests. The reason
    # is that soong interprets any output on stderr as an error and marks the
    # unit test as failed although the test itself succeeded.
    self.stderr = sys.stderr
    self.null = open(os.devnull, 'wb')
    sys.stderr = self.null

    # Test AftlIcpEntry #1
    self.test_tl_url_1 = 'aftl-test-server.google.com'

    self.test_sth_1 = aftltool.TrillianLogRootDescriptor()
    self.test_sth_1.tree_size = 2
    self.test_sth_1.root_hash_size = 32
    self.test_sth_1.root_hash = bytearray('f' * 32)
    self.test_sth_1.timestamp = 0x1234567890ABCDEF
    self.test_sth_1.revision = 0xFEDCBA0987654321

    self.test_sth_1_bytes = bytearray(
        '\x00\x01'                          # version
        '\x00\x00\x00\x00\x00\x00\x00\x02'  # tree_size
        '\x20'                              # root_hash_size
        + 'f' * 32 +                        # root_hash
        '\x12\x34\x56\x78\x90\xAB\xCD\xEF'  # timestamp
        '\xFE\xDC\xBA\x09\x87\x65\x43\x21'  # revision
        '\x00\x00'                          # metadata_size
        ''                                  # metadata (empty)
    )

    # Fill each structure with an easily observable pattern for easy validation.
    self.test_proof_hashes_1 = []
    self.test_proof_hashes_1.append(bytearray('b' * 32))
    self.test_proof_hashes_1.append(bytearray('c' * 32))
    self.test_proof_hashes_1.append(bytearray('d' * 32))
    self.test_proof_hashes_1.append(bytearray('e' * 32))

    # Valid test AftlIcpEntry #1.
    self.test_entry_1 = aftltool.AftlIcpEntry()
    self.test_entry_1.set_log_url(self.test_tl_url_1)
    self.test_entry_1.leaf_index = 1
    self.test_entry_1.set_log_root_descriptor(self.test_sth_1)
    self.test_entry_1.set_proofs(self.test_proof_hashes_1)
    self.test_entry_1.log_root_signature = 'g' * 512  # bytearray('g' * 512)
    self.test_entry_1.log_root_sig_size = 512

    self.test_entry_1_bytes = bytearray(
        '\x00\x00\x00\x1b'                  # Transparency log url size.
        '\x00\x00\x00\x00\x00\x00\x00\x01'  # Leaf index.
        '\x00\x00\x00\x3d'                  # Log root descriptor size.
        '\x00\x00\x00\x00'                  # Firmware info leaf size.
        '\x02\x00'                          # Log root signature size.
        '\x04'                              # Number of hashes in ICP.
        '\x00\x00\x00\x80'                  # Size of ICP in bytes.
        'aftl-test-server.google.com'       # Transparency log url.
        + self.test_sth_1_bytes
        + 'g' * 512                         # Log root signature.
        + 'b' * 32                          # Hashes...
        + 'c' * 32
        + 'd' * 32
        + 'e' * 32)

    # Valid test AftlIcpEntry #2.
    self.test_tl_url_2 = 'aftl-test-server.google.ch'

    self.test_sth_2 = aftltool.TrillianLogRootDescriptor()
    self.test_sth_2.tree_size = 4
    self.test_sth_2.root_hash_size = 32
    self.test_sth_2.root_hash = bytearray('e' * 32)
    self.test_sth_2.timestamp = 6
    self.test_sth_2.revision = 7
    self.test_sth_2.metadata_size = 2
    self.test_sth_2.metadata = '12'

    self.test_sth_2_bytes = bytearray(
        '\x00\x01'                          # version
        '\x00\x00\x00\x00\x00\x00\x00\x04'  # tree_size
        '\x20'                              # root_hash_size
        + 'e' * 32 +                        # root_hash
        '\x00\x00\x00\x00\x00\x00\x00\x06'  # timestamp
        '\x00\x00\x00\x00\x00\x00\x00\x07'  # revision
        '\x00\x02'                          # metadata_size
        '12'                                # metadata
    )

    # Fill each structure with an easily observable pattern for easy validation.
    self.test_proof_hashes_2 = []
    self.test_proof_hashes_2.append(bytearray('g' * 32))
    self.test_proof_hashes_2.append(bytearray('h' * 32))

    self.test_entry_2 = aftltool.AftlIcpEntry()
    self.test_entry_2.set_log_url(self.test_tl_url_2)
    self.test_entry_2.leaf_index = 2
    self.test_entry_2.set_log_root_descriptor(self.test_sth_2)
    self.test_entry_2.log_root_signature = bytearray('d' * 512)
    self.test_entry_2.log_root_sig_size = 512
    self.test_entry_2.set_proofs(self.test_proof_hashes_2)

    self.test_entry_2_bytes = bytearray(
        '\x00\x00\x00\x1a'                  # Transparency log url size.
        '\x00\x00\x00\x00\x00\x00\x00\x02'  # Leaf index.
        '\x00\x00\x00\x3f'                     # Log root descriptor size.
        '\x00\x00\x00\x00'                  # Firmware info leaf size.
        '\x02\x00'                          # Log root signature size.
        '\x02'                              # Number of hashes in ICP.
        '\x00\x00\x00@'                     # Size of ICP in bytes.
        'aftl-test-server.google.ch'        # Transparency log url.
        + self.test_sth_2_bytes             # Log root
        + 'd' * 512                         # Log root signature.
        + 'g' * 32                          # Hashes...
        + 'h' * 32)

    # Valid test AftlDescriptor made out of AftlEntry #1 and #2.
    self.test_aftl_desc = aftltool.AftlDescriptor()
    self.test_aftl_desc.add_icp_entry(self.test_entry_1)
    self.test_aftl_desc.add_icp_entry(self.test_entry_2)

    self.test_expected_aftl_descriptor_bytes = bytearray(
        # AftlIcpHeader
        'AFTL'                              # Magic.
        '\x00\x00\x00\x01'                  # Descriptor size.
        '\x00\x00\x00\x01'                  # Major version.
        '\x00\x00\x00\x12'                  # Minor version.
        '\x00\x02'                          # Number of ICP entries.
        + self.test_entry_1_bytes
        + self.test_entry_2_bytes)

    # Sets up test data.
    # pylint: disable=no-member
    self.test_afi_resp = proto.api_pb2.AddFirmwareInfoResponse()
    self.test_afi_resp.fw_info_proof.proof.leaf_index = 6263
    hashes = [
        '3ad99869646980c0a51d637a9791f892d12e0bc83f6bac5d305a9e289e7f7e8b',
        '2e5c664d2aee64f71cb4d292e787d0eae7ca9ed80d1e08abb41d26baca386c05',
        'a671dd99f8d97e9155cc2f0a9dc776a112a5ec5b821ec71571bb258ac790717a',
        '78046b839595e4e49ad4b0c73f92bf4803aacd4a3351181086509d057ef0d7a9',
        'c0a7e013f03e7c69e9402070e113dadb345868cf144ccb174fabc384b5605abf',
        'dc36e5dbe36abe9f4ad10f14170aa0148b6fe3fcaba9df43deaf4dede01b02e8',
        'b063e7fb665370a361718208756c363dc5206e2e9af9b4d847d81289cdae30de',
        'a69ea5ba88a221103636d3f4245c800570eb86ad9276121481521f97d0a04a81']
    for h in hashes:
      self.test_afi_resp.fw_info_proof.proof.hashes.append(
          binascii.unhexlify(h))
    self.test_afi_resp.fw_info_proof.sth.key_hint = binascii.unhexlify(
        '5af859abce8fe1ea')
    self.test_afi_resp.fw_info_proof.sth.log_root = binascii.unhexlify(
        '000100000000000018782053b182b55dc1377197c938637f50093131daea4'
        'd0696b1eae5b8a014bfde884a15edb28f1fc7954400000000000013a50000'
    )
    self.test_afi_resp.vbmeta_proof.sth.log_root_signature = binascii.unhexlify(
        'c264bc7986a1cf56364ca4dd04989f45515cb8764d05b4fb2b880172585ea404'
        '2105f95a0e0471fb6e0f8c762b14b2e526fb78eaddcc61484917795a12f6ab3b'
        '557b5571d492d07d7950595f9ad8647a606c7c633f4697c5eb59c272aeca0419'
        '397c70a3b9b51537537c4ea6b49d356110e70a9286902f814cc6afbeafe612e4'
        '9e180146140e902bdd9e9dae66b37b4943150a9571949027a648db88a4eea3ad'
        'f930b4fa6a183e97b762ab0e55a3a26aa6b0fd44d30531e2541ecb94bf645e62'
        '59e8e3151e7c3b51a09fe24557ce2fd2c0ecdada7ce99c390d2ef10e5d075801'
        '7c10d49c55cdee930959cc35f0104e04f296591eeb5defbc9ebb237da7b204ca'
        'a4608cb98d6bc3a01f18585a04441caf8ec7a35aa2d35f7483b92b14fd0f4a41'
        '3a91133545579309adc593222ca5032a103b00d8fcaea911936dbec11349e4dd'
        '419b091ea7d1130570d70e2589dd9445fd77fd7492507e1c87736847b9741cc6'
        '236868af42558ff6e833e12010c8ede786e43ada40ff488f5f1870d1619887d7'
        '66a24ad0a06a47cc14e2f7db07361be191172adf3155f49713807c7c265f5a84'
        '040fc84246ccf7913e44721f0043cea05ee774e457e13206775eee992620c3f9'
        'd2b2584f58aac19e4afe35f0a17df699c45729f94101083f9fc4302659a7e6e0'
        'e7eb36f8d1ca0be2c9010160d329bd2d17bb707b010fdd63c30b667a0b886cf9'
    )
    self.test_afi_resp.fw_info_leaf = (
        '{\"timestamp\":{\"seconds\":1580115370,\"nanos\":621454825},\"Va'
        'lue\":{\"FwInfo\":{\"info\":{\"info\":{\"vbmeta_hash\":\"ViNzEQS'
        '/oc/bJ13yl40fk/cvXw90bxHQbzCRxgHDIGc=\",\"version_incremental\":'
        '\"1\",\"manufacturer_key_hash\":\"yBCrUOdjvaAh4git5EgqWa5neegUao'
        'XeLlB67+N8ObY=\"}}}}}')

  def tearDown(self):
    """Tears down the test bed for the unit tests."""
    # Reconnects stderr back to the normal stderr; see setUp() for details.
    sys.stderr = self.stderr

    super(AftltoolTestCase, self).setUp()


class AftltoolTest(AftltoolTestCase):

  def setUp(self):
    """Sets up the test bed for the unit tests."""
    super(AftltoolTest, self).setUp()

    self.test_url = 'test'
    self.test_sth = aftltool.TrillianLogRootDescriptor()
    self.test_sth.leaf_hash = bytearray('leaf' * 8)
    self.test_sth.tree_size = 2
    self.test_sth.root_hash = bytearray('root' * 8)
    self.test_sth.root_hash_size = 32
    self.test_sth.log_root_sig = bytearray('root_sig' * 64)
    self.test_proofs = 'proofs'

  def _validate_icp_entry_with_setters(
      self, log_url, leaf_index, log_root_descriptor, proofs):
    """Create an ICP entry structure and attempt to validate it.

    Returns:
      True if the tests pass, False otherwise.
    """
    icp_entry = aftltool.AftlIcpEntry()
    icp_entry.leaf_index = leaf_index
    icp_entry.set_log_url(log_url)
    icp_entry.set_log_root_descriptor(log_root_descriptor)
    icp_entry.set_proofs(proofs)
    return icp_entry.is_valid()

  def _validate_icp_entry_without_setters(
      self, log_url, log_url_size, leaf_index, log_root_descriptor,
      log_root_descriptor_size, proof_hash_count, proofs, inc_proof_size):
    """Create an ICP entry structure and attempt to validate it.

    Returns:
      True if the tests pass, False otherwise.
    """
    icp_entry = aftltool.AftlIcpEntry()
    icp_entry.log_url = log_url
    icp_entry.log_url_size = log_url_size
    icp_entry.leaf_index = leaf_index
    icp_entry.log_root_descriptor = log_root_descriptor
    icp_entry.log_root_descriptor_size = log_root_descriptor_size
    icp_entry.proof_hash_count = proof_hash_count
    icp_entry.proofs = proofs
    icp_entry.inc_proof_size = inc_proof_size
    return icp_entry.is_valid()

  def test_default_icp_entry(self):
    """Tests default ICP entry structure."""
    icp_entry = aftltool.AftlIcpEntry()
    self.assertTrue(icp_entry.is_valid())

  def test_icp_entry_valid(self):
    """Tests valid ICP entry structures."""
    self.assertTrue(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.get_expected_size(), 2, self.test_proofs,
            len(self.test_proofs)))

    self.assertTrue(
        self._validate_icp_entry_with_setters(
            self.test_url, 2, self.test_sth, self.test_proofs))

    self.assertTrue(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.get_expected_size(), 2, self.test_proofs,
            len(self.test_proofs)))

    self.assertTrue(
        self._validate_icp_entry_with_setters(
            self.test_url, 2, self.test_sth, self.test_proofs))

  def test_icp_entry_invalid_log_url(self):
    """Tests ICP entry with invalid log_url / log_url_size combination."""
    self.assertFalse(
        self._validate_icp_entry_without_setters(
            None, 10, 2, self.test_sth, self.test_sth.get_expected_size(),
            2, self.test_proofs, len(self.test_proofs)))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            '', 10, 2, self.test_sth, self.test_sth.get_expected_size(),
            2, self.test_proofs, len(self.test_proofs)))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, -2, 2, self.test_sth,
            self.test_sth.get_expected_size(),
            2, self.test_proofs, len(self.test_proofs)))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url) - 3, 2, self.test_sth,
            self.test_sth.get_expected_size(), 2, self.test_proofs,
            len(self.test_proofs)))

  def test_icp_entry_invalid_leaf_index(self):
    """Tests ICP entry with invalid leaf_index."""
    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), -1, self.test_sth,
            self.test_sth.get_expected_size(), 2, self.test_proofs,
            len(self.test_proofs)))

  def test_icp_entry_invalid_sth(self):
    """Tests ICP entry with invalid STH / STH length."""
    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, None, 3,
            2, self.test_proofs, len(self.test_proofs)))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, '', 3,
            2, self.test_proofs, len(self.test_proofs)))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, bytearray(), 3,
            2, self.test_proofs, len(self.test_proofs)))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth, -2,
            2, self.test_proofs, len(self.test_proofs)))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2,
            self.test_sth, self.test_sth.get_expected_size() + 14,
            2, self.test_proofs, len(self.test_proofs)))

  def test_icp_entry_invalid_proof_hash_count(self):
    """Tests ICP entry with invalid proof_hash_count."""
    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.get_expected_size(), -2, self.test_proofs,
            len(self.test_proofs)))

  def test_icp_entry_invalid_proofs(self):
    """Tests ICP entry with invalid proofs / proof size."""
    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.get_expected_size(), 2, [], len(self.test_proofs)))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.get_expected_size(), 2, '', len(self.test_proofs)))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.get_expected_size(), 2, bytearray(),
            len(self.test_proofs)))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.get_expected_size(), 2, self.test_proofs,
            len(self.test_proofs) - 3))

  def test_merkle_root_hash(self):
    """Tests validation of inclusion proof and the merkle tree calculations.

    The test vectors have been taken from the Trillian tests:
    https://github.com/google/trillian/blob/v1.3.3/merkle/log_verifier_test.go
    """

    inclusion_proofs = [
        (1,
         8,
         [
             binascii.unhexlify('96a296d224f285c67bee93c30f8a3091'
                                '57f0daa35dc5b87e410b78630a09cfc7'),
             binascii.unhexlify('5f083f0a1a33ca076a95279832580db3'
                                'e0ef4584bdff1f54c8a360f50de3031e'),
             binascii.unhexlify('6b47aaf29ee3c2af9af889bc1fb9254d'
                                'abd31177f16232dd6aab035ca39bf6e4')
         ]),
        (6,
         8,
         [
             binascii.unhexlify('bc1a0643b12e4d2d7c77918f44e0f4f7'
                                '9a838b6cf9ec5b5c283e1f4d88599e6b'),
             binascii.unhexlify('ca854ea128ed050b41b35ffc1b87b8eb'
                                '2bde461e9e3b5596ece6b9d5975a0ae0'),
             binascii.unhexlify('d37ee418976dd95753c1c73862b9398f'
                                'a2a2cf9b4ff0fdfe8b30cd95209614b7')
         ]),
        (3,
         3,
         [
             binascii.unhexlify('fac54203e7cc696cf0dfcb42c92a1d9d'
                                'baf70ad9e621f4bd8d98662f00e3c125')
         ]),
        (2,
         5,
         [
             binascii.unhexlify('6e340b9cffb37a989ca544e6bb780a2c'
                                '78901d3fb33738768511a30617afa01d'),
             binascii.unhexlify('5f083f0a1a33ca076a95279832580db3'
                                'e0ef4584bdff1f54c8a360f50de3031e'),
             binascii.unhexlify('bc1a0643b12e4d2d7c77918f44e0f4f7'
                                '9a838b6cf9ec5b5c283e1f4d88599e6b')
         ]
        )
    ]

    leaves = [
        binascii.unhexlify(''),
        binascii.unhexlify('00'),
        binascii.unhexlify('10'),
        binascii.unhexlify('2021'),
        binascii.unhexlify('3031'),
        binascii.unhexlify('40414243'),
        binascii.unhexlify('5051525354555657'),
        binascii.unhexlify('606162636465666768696a6b6c6d6e6f'),
    ]

    roots = [
        binascii.unhexlify('6e340b9cffb37a989ca544e6bb780a2c'
                           '78901d3fb33738768511a30617afa01d'),
        binascii.unhexlify('fac54203e7cc696cf0dfcb42c92a1d9d'
                           'baf70ad9e621f4bd8d98662f00e3c125'),
        binascii.unhexlify('aeb6bcfe274b70a14fb067a5e5578264'
                           'db0fa9b51af5e0ba159158f329e06e77'),
        binascii.unhexlify('d37ee418976dd95753c1c73862b9398f'
                           'a2a2cf9b4ff0fdfe8b30cd95209614b7'),
        binascii.unhexlify('4e3bbb1f7b478dcfe71fb631631519a3'
                           'bca12c9aefca1612bfce4c13a86264d4'),
        binascii.unhexlify('76e67dadbcdf1e10e1b74ddc608abd2f'
                           '98dfb16fbce75277b5232a127f2087ef'),
        binascii.unhexlify('ddb89be403809e325750d3d263cd7892'
                           '9c2942b7942a34b77e122c9594a74c8c'),
        binascii.unhexlify('5dc9da79a70659a9ad559cb701ded9a2'
                           'ab9d823aad2f4960cfe370eff4604328'),
    ]

    for icp in inclusion_proofs:
      leaf_id = icp[0] - 1
      leaf_hash = aftltool.rfc6962_hash_leaf(leaves[leaf_id])
      root_hash = aftltool.root_from_icp(leaf_id, icp[1], icp[2], leaf_hash)
      self.assertEqual(root_hash, roots[icp[1] -1])


class AftlDescriptorTest(AftltoolTestCase):

  def test__init__(self):
    """Tests the constructor."""
    # Calls constructor without data.
    d = aftltool.AftlDescriptor()
    self.assertTrue(isinstance(d.icp_header, aftltool.AftlIcpHeader))
    self.assertEqual(d.icp_header.icp_count, 0)
    self.assertEqual(d.icp_entries, [])
    self.assertTrue(d.is_valid())

    # Calls constructor with data.
    d = aftltool.AftlDescriptor(self.test_expected_aftl_descriptor_bytes)
    self.assertTrue(isinstance(d.icp_header, aftltool.AftlIcpHeader))
    self.assertEqual(d.icp_header.icp_count, 2)
    self.assertEqual(len(d.icp_entries), 2)
    for entry in d.icp_entries:
      self.assertTrue(isinstance(entry, aftltool.AftlIcpEntry))
    self.assertTrue(d.is_valid())

  def test_add_icp_entry(self):
    """Tests the add_icp_entry method."""
    d = aftltool.AftlDescriptor()

    # Adds 1st ICP.
    d.add_icp_entry(self.test_entry_1)
    self.assertEqual(d.icp_header.icp_count, 1)
    self.assertEqual(len(d.icp_entries), 1)
    self.assertTrue(d.is_valid())

    # Adds 2nd ICP.
    d.add_icp_entry(self.test_entry_2)
    self.assertEqual(d.icp_header.icp_count, 2)
    self.assertEqual(len(d.icp_entries), 2)
    self.assertTrue(d.is_valid())

  def test_save(self):
    """Tests save method."""
    buf = io.BytesIO()
    self.test_aftl_desc.save(buf)
    self.assertEqual(buf.getvalue(), self.test_expected_aftl_descriptor_bytes)

  def test_encode(self):
    """Tests encode method."""
    desc_bytes = self.test_aftl_desc.encode()
    self.assertEqual(desc_bytes, self.test_expected_aftl_descriptor_bytes)

  def test_is_valid(self):
    """Tests is_valid method."""
    d = aftltool.AftlDescriptor()
    d.add_icp_entry(self.test_entry_1)
    d.add_icp_entry(self.test_entry_2)

    # Force invalid icp header
    old_magic = d.icp_header.magic
    d.icp_header.magic = 'YOLO'
    self.assertFalse(d.is_valid())
    d.icp_header.magic = old_magic
    self.assertTrue(d.is_valid())

    # Force count mismatch between header and actual entries.
    old_icp_count = d.icp_header.icp_count
    d.icp_header.icp_count = 1
    self.assertFalse(d.is_valid())
    d.icp_header.icp_count = old_icp_count
    self.assertTrue(d.is_valid())

    # Force invalid icp_entry.
    old_log_url_size = d.icp_entries[0].log_url_size
    d.icp_entries[0].log_url_size = 0
    self.assertFalse(d.is_valid())
    d.icp_entries[0].log_url_size = old_log_url_size
    self.assertTrue(d.is_valid())

  def test_print_desc(self):
    """Tests print_desc method."""
    buf = io.BytesIO()
    self.test_aftl_desc.print_desc(buf)
    desc = buf.getvalue()

    # Cursory check whether the printed description contains something useful.
    self.assertGreater(len(desc), 0)
    self.assertTrue('Log Root Descriptor:' in desc)


class AftlIcpHeaderTest(AftltoolTestCase):
  """Test suite for testing the AftlIcpHeader descriptor."""

  def setUp(self):
    """Sets up the test bed for the unit tests."""
    super(AftlIcpHeaderTest, self).setUp()

    self.test_header_valid = aftltool.AftlIcpHeader()
    self.test_header_valid.icp_count = 1

    self.test_header_invalid = aftltool.AftlIcpHeader()
    self.test_header_invalid.icp_count = -34

    self.test_header_bytes = bytearray('\x41\x46\x54\x4c\x00\x00\x00\x01'
                                       '\x00\x00\x00\x01\x00\x00\x00\x12'
                                       '\x00\x01')

  def test__init__(self):
    """Tests default ICP header structure."""

    # Calls constructor without data.
    header = aftltool.AftlIcpHeader()
    self.assertEqual(header.magic, 'AFTL')
    self.assertEqual(header.required_icp_version_major,
                     avbtool.AVB_VERSION_MAJOR)
    self.assertEqual(header.required_icp_version_minor,
                     avbtool.AVB_VERSION_MINOR)
    self.assertEqual(header.aftl_descriptor_size, aftltool.AftlIcpHeader.SIZE)
    self.assertEqual(header.icp_count, 0)
    self.assertTrue(header.is_valid())

    # Calls constructor with data.
    header = aftltool.AftlIcpHeader(self.test_header_bytes)
    self.assertEqual(header.magic, 'AFTL')
    self.assertEqual(header.required_icp_version_major, 1)
    self.assertEqual(header.required_icp_version_minor, 1)
    self.assertEqual(header.aftl_descriptor_size, aftltool.AftlIcpHeader.SIZE)
    self.assertTrue(header.icp_count, 1)
    self.assertTrue(header.is_valid())

  def test_save(self):
    """Tests ICP header save method."""
    buf = io.BytesIO()
    self.test_header_valid.save(buf)
    self.assertEqual(buf.getvalue(), self.test_header_bytes)

  def test_encode(self):
    """Tests ICP header encoding."""
    # Valid header.
    header_bytes = self.test_header_valid.encode()
    self.assertEqual(header_bytes, self.test_header_bytes)

    # Invalid header
    with self.assertRaises(aftltool.AftlError):
      header_bytes = self.test_header_invalid.encode()

  def test_is_valid(self):
    """Tests valid ICP header structures."""
    # Invalid magic.
    header = aftltool.AftlIcpHeader()
    self.assertTrue(header.is_valid())

    # Invalid magic.
    header = aftltool.AftlIcpHeader()
    header.magic = 'YOLO'
    self.assertFalse(header.is_valid())

    # Valid ICP count.
    self.assertTrue(self.test_header_valid.is_valid())

    # Invalid ICP count.
    self.assertFalse(self.test_header_invalid.is_valid())

    header = aftltool.AftlIcpHeader()
    header.icp_count = 10000000
    self.assertFalse(header.is_valid())

    # Invalid ICP major version.
    header = aftltool.AftlIcpHeader()
    header.required_icp_version_major = avbtool.AVB_VERSION_MAJOR + 1
    self.assertFalse(header.is_valid())

    # Invalid ICP minor version.
    header = aftltool.AftlIcpHeader()
    header.required_icp_version_minor = avbtool.AVB_VERSION_MINOR + 1
    self.assertFalse(header.is_valid())

  def test_print_desc(self):
    """Tests print_desc method."""
    buf = io.BytesIO()
    self.test_header_valid.print_desc(buf)
    desc = buf.getvalue()

    # Cursory check whether the printed description contains something useful.
    self.assertGreater(len(desc), 0)
    self.assertTrue('Major version:' in desc)


class TrillianLogRootDescriptorTest(AftltoolTestCase):
  """Test suite for testing the TrillianLogRootDescriptorTest descriptor."""

  def setUp(self):
    """Sets up the test bed for the unit tests."""
    super(TrillianLogRootDescriptorTest, self).setUp()

    # Creates basic log root without metadata fields.
    base_log_root = (
        '0001'                              # version
        '00000000000002e5'                  # tree_size
        '20'                                # root_hash_size
        '2d614759ad408a111a3351c0cb33c099'  # root_hash
        '422c30a5c5104788a343332bde2b387b'
        '15e1c97e3b4bd239'                  # timestamp
        '00000000000002e4'                  # revision
    )

    # Create valid log roots with metadata fields w/ and w/o metadata.
    self.test_log_root_bytes_wo_metadata = binascii.unhexlify(
        base_log_root + '0000')
    self.test_log_root_bytes_with_metadata = binascii.unhexlify(
        base_log_root + '00023132')

  def test__init__(self):
    """Tests constructor."""
    # Calls constructor without data.
    d = aftltool.TrillianLogRootDescriptor()
    self.assertTrue(d.is_valid())
    self.assertEqual(d.version, 1)
    self.assertEqual(d.tree_size, 0)
    self.assertEqual(d.root_hash_size, 0)
    self.assertEqual(d.root_hash, bytearray())
    self.assertEqual(d.timestamp, 0)
    self.assertEqual(d.revision, 0)
    self.assertEqual(d.metadata_size, 0)
    self.assertEqual(d.metadata, bytearray())

    # Calls constructor with log_root w/o metadata
    d = aftltool.TrillianLogRootDescriptor(self.test_log_root_bytes_wo_metadata)
    self.assertTrue(d.is_valid())
    self.assertEqual(d.version, 1)
    self.assertEqual(d.tree_size, 741)
    self.assertEqual(d.root_hash_size, 32)
    self.assertEqual(d.root_hash,
                     binascii.unhexlify('2d614759ad408a111a3351c0cb33c099'
                                        '422c30a5c5104788a343332bde2b387b'))
    self.assertEqual(d.timestamp, 1576762888554271289)
    self.assertEqual(d.revision, 740)
    self.assertEqual(d.metadata_size, 0)
    self.assertEqual(d.metadata, bytearray())

    # Calls constructor with log_root with metadata
    d = aftltool.TrillianLogRootDescriptor(
        self.test_log_root_bytes_with_metadata)
    self.assertEqual(d.metadata_size, 2)
    self.assertEqual(d.metadata, bytearray('12'))

  def test_get_expected_size(self):
    """Tests get_expected_size method."""
    # Default constructor.
    d = aftltool.TrillianLogRootDescriptor()
    self.assertEqual(d.get_expected_size(), 11 + 18)

    # Log root without metadata.
    d = aftltool.TrillianLogRootDescriptor(self.test_log_root_bytes_wo_metadata)
    self.assertEqual(d.get_expected_size(), 11 + 18 + 32)

    # Log root with metadata.
    d = aftltool.TrillianLogRootDescriptor(
        self.test_log_root_bytes_with_metadata)
    self.assertEqual(d.get_expected_size(), 11 + 18 + 32 + 2)

  def test_encode(self):
    """Tests encode method."""
    # Log root from default constructor.
    d = aftltool.TrillianLogRootDescriptor()
    expected_bytes = (
        '0001'                              # version
        '0000000000000000'                  # tree_size
        '00'                                # root_hash_size
        ''                                  # root_hash (empty)
        '0000000000000000'                  # timestamp
        '0000000000000000'                  # revision
        '0000'                              # metadata size
        ''                                  # metadata (empty)
    )
    self.assertEqual(d.encode(), binascii.unhexlify(expected_bytes))

    # Log root without metadata.
    d = aftltool.TrillianLogRootDescriptor(self.test_log_root_bytes_wo_metadata)
    self.assertEqual(d.encode(), self.test_log_root_bytes_wo_metadata)

    # Log root with metadata.
    d = aftltool.TrillianLogRootDescriptor(
        self.test_log_root_bytes_with_metadata)
    self.assertEqual(d.encode(), self.test_log_root_bytes_with_metadata)

  def test_is_valid(self):
    """Tests the is_valid method."""
    d = aftltool.TrillianLogRootDescriptor()
    self.assertTrue(d.is_valid())

    # Invalid version.
    d = aftltool.TrillianLogRootDescriptor()
    d.version = 2
    self.assertFalse(d.is_valid())

    # Invalid tree_size.
    d = aftltool.TrillianLogRootDescriptor()
    d.tree_size = -1
    self.assertFalse(d.is_valid())

    # Invalid root_hash_size.
    d = aftltool.TrillianLogRootDescriptor()
    d.root_hash_size = -1
    self.assertFalse(d.is_valid())
    d.root_hash_size = 300
    self.assertFalse(d.is_valid())

    # Invalid/valid root_hash_size / root_hash combination.
    d = aftltool.TrillianLogRootDescriptor()
    d.root_hash_size = 4
    d.root_hash = '123'
    self.assertFalse(d.is_valid())
    d.root_hash = '1234'
    self.assertTrue(d.is_valid())

    # Invalid timestamp.
    d = aftltool.TrillianLogRootDescriptor()
    d.timestamp = -1
    self.assertFalse(d.is_valid())

    # Invalid revision.
    d = aftltool.TrillianLogRootDescriptor()
    d.revision = -1
    self.assertFalse(d.is_valid())

    # Invalid metadata_size.
    d = aftltool.TrillianLogRootDescriptor()
    d.metadata_size = -1
    self.assertFalse(d.is_valid())
    d.metadata_size = 70000
    self.assertFalse(d.is_valid())

    # Invalid/valid metadata_size / metadata combination.
    d = aftltool.TrillianLogRootDescriptor()
    d.metadata_size = 4
    d.metadata = '123'
    self.assertFalse(d.is_valid())
    d.metadata = '1234'
    self.assertTrue(d.is_valid())

  def test_print_desc(self):
    """Tests print_desc method."""
    # Log root without metadata
    buf = io.BytesIO()
    d = aftltool.TrillianLogRootDescriptor(self.test_log_root_bytes_wo_metadata)
    d.print_desc(buf)
    desc = buf.getvalue()

    # Cursory check whether the printed description contains something useful.
    self.assertGreater(len(desc), 0)
    self.assertTrue('Version:' in desc)
    self.assertFalse('Metadata:' in desc)

    # Log root with metadata
    buf = io.BytesIO()
    d = aftltool.TrillianLogRootDescriptor(
        self.test_log_root_bytes_with_metadata)
    d.print_desc(buf)
    desc = buf.getvalue()

    # Cursory check whether the printed description contains something useful.
    self.assertGreater(len(desc), 0)
    self.assertTrue('Version:' in desc)
    self.assertTrue('Metadata:' in desc)


class AftlMockCommunication(aftltool.AftlCommunication):
  """Testing Mock implementation of AftlCommunication."""

  def __init__(self, transparency_log, canned_response):
    """Initializes the object.

    Arguments:
      transparency_log: String containing the URL of a transparency log server.
      canned_response: AddFirmwareInfoResponse to return or the Exception to
        raise.
    """
    super(AftlMockCommunication, self).__init__(transparency_log)
    self.request = None
    self.canned_response = canned_response

  def AddFirmwareInfo(self, request):
    """Records the request and returns the canned response."""
    self.request = request

    if isinstance(self.canned_response, aftltool.AftlError):
      raise self.canned_response
    return self.canned_response


class AftlTest(AftltoolTestCase):

  def setUp(self):
    """Sets up the test bed for the unit tests."""
    super(AftlTest, self).setUp()
    self.mock_aftl_host = 'test.foo.bar:9000'

  # pylint: disable=no-member
  def test_request_inclusion_proof(self):
    """Tests the request_inclusion_proof method."""
    aftl_comms = AftlMockCommunication(self.mock_aftl_host, self.test_afi_resp)
    aftl = aftltool.Aftl()
    icp = aftl.request_inclusion_proof(self.mock_aftl_host,
                                       'a'*1024, 'version_inc',
                                       'test/data/testkey_rsa4096.pem',
                                       None, None,
                                       aftl_comms=aftl_comms)
    self.assertEqual(icp.leaf_index,
                     self.test_afi_resp.fw_info_proof.proof.leaf_index)
    self.assertEqual(icp.proof_hash_count,
                     len(self.test_afi_resp.fw_info_proof.proof.hashes))
    self.assertEqual(icp.log_url, self.mock_aftl_host)
    self.assertEqual(
        icp.log_root_descriptor.root_hash, binascii.unhexlify(
            '53b182b55dc1377197c938637f50093131daea4d0696b1eae5b8a014bfde884a'))

    self.assertEqual(icp.fw_info_leaf.version_incremental, 'version_inc')
    # To calculate the hash of the a RSA key use the following command:
    # openssl rsa -in test/data/testkey_rsa4096.pem -pubout \
    #    -outform DER | sha256sum
    self.assertEqual(icp.fw_info_leaf.manufacturer_key_hash, binascii.unhexlify(
        '9841073d16a7abbe21059e026da71976373d8f74fdb91cc46aa0a7d622b925b9'))

    self.assertEqual(icp.log_root_signature,
                     self.test_afi_resp.fw_info_proof.sth.log_root_signature)
    self.assertEqual(icp.proofs, self.test_afi_resp.fw_info_proof.proof.hashes)

  # pylint: disable=no-member
  def test_request_inclusion_proof_failure(self):
    """Tests the request_inclusion_proof_method in case of a comms problem."""
    aftl_comms = AftlMockCommunication(self.mock_aftl_host,
                                       aftltool.AftlError('Comms error'))
    aftl = aftltool.Aftl()
    with self.assertRaises(aftltool.AftlError):
      aftl.request_inclusion_proof(self.mock_aftl_host,
                                   'a'*1024, 'version_inc',
                                   'test/data/testkey_rsa4096.pem',
                                   None, None,
                                   aftl_comms=aftl_comms)

if __name__ == '__main__':
  unittest.main(verbosity=2)

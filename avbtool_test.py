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
"""Unit tests for avbtool."""

# pylint: disable=unused-import
from __future__ import print_function

import binascii
import os
import sys
import unittest

import avbtool


class AvbtoolTest(unittest.TestCase):

  def setUp(self):
    """Sets up the test bed for the unit tests."""
    super(AvbtoolTest, self).setUp()

    self.test_url = 'test'
    self.test_sth = avbtool.AvbIcpSignedRootBlob()
    self.test_sth.leaf_hash = bytearray('leaf' * 8)
    self.test_sth.tree_size = 2
    self.test_sth.root_hash = bytearray('root' * 8)
    self.test_sth.log_root_sig = bytearray('root_sig' * 64)
    self.test_proofs = 'proofs'

    # Redirects the stderr to /dev/null when running the unittests. The reason
    # is that soong interprets any output on stderr as an error and marks the
    # unit test as failed although the test itself succeeded.
    self.stderr = sys.stderr
    self.null = open(os.devnull, 'wb')
    sys.stderr = self.null

  def tearDown(self):
    """Tears down the test bed for the unit tests."""
    # Reconnects stderr back to the normal stderr; see setUp() for details.
    sys.stderr = self.stderr

    super(AvbtoolTest, self).tearDown()

  def _validate_icp_header(self, algorithm, icp_count):
    """Validate an ICP header structure and attempt to validate it.

    Arguments:
      algorithm: The algorithm to be used.
      icp_count: Number of ICPs that follow the ICP header.

    Returns:
      True if the ICP header validates; otherwise False.
    """
    icp_header = avbtool.AvbIcpHeader()
    icp_header.algorithm = algorithm
    icp_header.icp_count = icp_count
    return icp_header.is_valid()

  def _validate_icp_entry_with_setters(
      self, log_url, leaf_index, signed_root_blob, proofs,
      next_entry):
    """Create an ICP entry structure and attempt to validate it.

    Returns:
      True if the tests pass, False otherwise.
    """
    icp_entry = avbtool.AvbIcpEntry()
    icp_entry.leaf_index = leaf_index
    icp_entry.next_entry = next_entry
    icp_entry.set_log_url(log_url)
    icp_entry.set_signed_root_blob(signed_root_blob)
    icp_entry.set_proofs(proofs)
    return icp_entry.is_valid()

  def _validate_icp_entry_without_setters(
      self, log_url, log_url_size, leaf_index, signed_root_blob,
      signed_root_blob_size, proof_hash_count, proofs, proof_size, next_entry):
    """Create an ICP entry structure and attempt to validate it.

    Returns:
      True if the tests pass, False otherwise.
    """
    icp_entry = avbtool.AvbIcpEntry()
    icp_entry.log_url = log_url
    icp_entry.log_url_size = log_url_size
    icp_entry.leaf_index = leaf_index
    icp_entry.signed_root_blob = signed_root_blob
    icp_entry.signed_root_blob_size = signed_root_blob_size
    icp_entry.proof_hash_count = proof_hash_count
    icp_entry.proofs = proofs
    icp_entry.proof_size = proof_size
    icp_entry.next_entry = next_entry
    return icp_entry.is_valid()

  def _validate_icp_signed_root_blob(self, leaf_hash, tree_size,
                                     root_hash, log_root_sig):
    """Create an ICP SignedRootBlob and attempt to validate it.

    Returns:
      True if the tests pass, False otherwise.
    """
    icp_signed_root_blob = avbtool.AvbIcpSignedRootBlob()
    icp_signed_root_blob.leaf_hash = leaf_hash
    icp_signed_root_blob.tree_size = tree_size
    icp_signed_root_blob.root_hash = root_hash
    icp_signed_root_blob.log_root_sig = log_root_sig
    return icp_signed_root_blob.is_valid()

  def test_default_icp_header(self):
    """Tests default ICP header structure."""
    icp_header = avbtool.AvbIcpHeader()
    self.assertTrue(icp_header.is_valid())

  def test_valid_icp_header(self):
    """Tests valid ICP header structures."""
    # 1 is SHA256/RSA4096
    self.assertTrue(self._validate_icp_header(algorithm=1, icp_count=4))

  def test_invalid_icp_header(self):
    """Tests invalid ICP header structures."""
    self.assertFalse(self._validate_icp_header(algorithm=-12, icp_count=4))
    self.assertFalse(self._validate_icp_header(algorithm=4, icp_count=-34))
    self.assertFalse(self._validate_icp_header(algorithm=10, icp_count=10))

  def test_default_icp_entry(self):
    """Tests default ICP entry structure."""
    icp_entry = avbtool.AvbIcpEntry()
    self.assertTrue(icp_entry.is_valid())

  def test_icp_entry_valid(self):
    """Tests valid ICP entry structures."""
    self.assertTrue(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.SIZE, 2, self.test_proofs, len(self.test_proofs), 0))

    self.assertTrue(
        self._validate_icp_entry_with_setters(
            self.test_url, 2, self.test_sth, self.test_proofs, 0))

    self.assertTrue(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.SIZE, 2, self.test_proofs, len(self.test_proofs), 1))

    self.assertTrue(
        self._validate_icp_entry_with_setters(
            self.test_url, 2, self.test_sth, self.test_proofs, 1))

  def test_icp_entry_invalid_log_url(self):
    """Tests ICP entry with invalid log_url / log_url_size combination."""
    self.assertFalse(
        self._validate_icp_entry_without_setters(
            None, 10, 2, self.test_sth, self.test_sth.SIZE,
            2, self.test_proofs, len(self.test_proofs), 0))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            '', 10, 2, self.test_sth, self.test_sth.SIZE,
            2, self.test_proofs, len(self.test_proofs), 0))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, -2, 2, self.test_sth, self.test_sth.SIZE,
            2, self.test_proofs, len(self.test_proofs), 0))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url) - 3, 2, self.test_sth,
            self.test_sth.SIZE, 2, self.test_proofs, len(self.test_proofs), 0))

  def test_icp_entry_invalid_leaf_index(self):
    """Tests ICP entry with invalid leaf_index."""
    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), -1, self.test_sth,
            self.test_sth.SIZE, 2, self.test_proofs, len(self.test_proofs), 1))

  def test_icp_entry_invalid_sth(self):
    """Tests ICP entry with invalid STH / STH length."""
    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, None, 3,
            2, self.test_proofs, len(self.test_proofs), 0))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, '', 3,
            2, self.test_proofs, len(self.test_proofs), 0))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, bytearray(), 3,
            2, self.test_proofs, len(self.test_proofs), 0))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth, -2,
            2, self.test_proofs, len(self.test_proofs), 0))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2,
            self.test_sth, self.test_sth.SIZE + 14,
            2, self.test_proofs, len(self.test_proofs), 0))

  def test_icp_entry_invalid_proof_hash_count(self):
    """Tests ICP entry with invalid proof_hash_count."""
    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.SIZE, -2, self.test_proofs, len(self.test_proofs), 1))

  def test_icp_entry_invalid_proofs(self):
    """Tests ICP entry with invalid proofs / proof size."""
    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.SIZE, 2, [], len(self.test_proofs), 0))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.SIZE, 2, '', len(self.test_proofs), 0))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.SIZE, 2, bytearray(), len(self.test_proofs), 0))

    self.assertFalse(
        self._validate_icp_entry_without_setters(
            self.test_url, len(self.test_url), 2, self.test_sth,
            self.test_sth.SIZE, 2, self.test_proofs,
            len(self.test_proofs) - 3, 0))

  def test_icp_entry_invalid_next_entry(self):
    """Tests ICP entry with invalid next_entry."""
    self.assertFalse(self._validate_icp_entry_without_setters(
        self.test_url, len(self.test_url), 2, self.test_sth, self.test_sth.SIZE,
        2, self.test_proofs, len(self.test_proofs), 2))

  def test_icp_signed_root_blob(self):
    """Tests ICP SignedRootBlob."""
    self.assertTrue(self._validate_icp_signed_root_blob(
        self.test_sth.leaf_hash, self.test_sth.tree_size,
        self.test_sth.root_hash, self.test_sth.log_root_sig))
    self.assertTrue(self._validate_icp_signed_root_blob(bytearray(), 0,
                                                        bytearray(),
                                                        bytearray()))
    self.assertFalse(self._validate_icp_signed_root_blob(
        bytearray(), self.test_sth.tree_size, self.test_sth.root_hash,
        self.test_sth.log_root_sig))
    self.assertFalse(self._validate_icp_signed_root_blob(
        self.test_sth.leaf_hash, -2, self.test_sth.root_hash,
        self.test_sth.log_root_sig))
    self.assertFalse(self._validate_icp_signed_root_blob(
        self.test_sth.leaf_hash, self.test_sth.tree_size, bytearray(),
        self.test_sth.log_root_sig))
    self.assertFalse(self._validate_icp_signed_root_blob(
        self.test_sth.leaf_hash, self.test_sth.tree_size,
        self.test_sth.root_hash, bytearray()))

  def test_generate_icp_images(self):
    """Test cases for full AFTL ICP structure generation."""
    icp_header = avbtool.AvbIcpHeader()
    icp_header.algorithm = 1
    icp_header.icp_count = 1

    # Tests ICP header encoding.
    expected_header_bytes = bytearray(b'\x41\x46\x54\x4c\x00\x00\x00\x01'
                                      '\x00\x00\x00\x01\x00\x00\x00\x01'
                                      '\x00\x01')
    icp_header_bytes = icp_header.encode()
    self.assertEqual(icp_header_bytes, expected_header_bytes)

    # Tests ICP header decoding.
    icp_header = avbtool.AvbIcpHeader(expected_header_bytes)
    self.assertTrue(icp_header.is_valid())

    tl_url = 'aftl-test-server.google.com'
    sth = avbtool.AvbIcpSignedRootBlob()
    sth.leaf_hash = bytearray('a' * 32)
    sth.tree_size = 2
    sth.root_hash = bytearray('f' * 32)
    sth.log_root_sig = 'g' * 512  # bytearray('g' * 512)

    # Fill each structure with an easily observable pattern for easy validation.
    proof_hashes = []
    proof_hashes.append(bytearray('b' * 32))
    proof_hashes.append(bytearray('c' * 32))
    proof_hashes.append(bytearray('d' * 32))
    proof_hashes.append(bytearray('e' * 32))
    self.assertTrue(self._validate_icp_entry_with_setters(
        tl_url, 1, sth, proof_hashes, 0))

    # Tests ICP entry encoding.
    icp_entry = avbtool.AvbIcpEntry()
    icp_entry.set_log_url(tl_url)
    icp_entry.leaf_index = 1
    icp_entry.set_signed_root_blob(sth)
    icp_entry.set_proofs(proof_hashes)
    icp_entry.next_entry = 0
    icp_bytes = icp_entry.encode()

    expected_entry_bytes = bytearray(b'\x00\x00\x00\x1b\x00\x00\x00\x00\x00\x00'
                                     '\x00\x01\x00\x00\x02\x85\x04\x00\x00\x00'
                                     '\x80\x00aftl-test-server.google.comaaaaaa'
                                     'aaaaaaaaaaaaaaaaaaaaaaaaaa\x00\x00\x00'
                                     '\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00'
                                     '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                     '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                     '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                     '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                     '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                     '\x00\x00\x00\x00\x00\x00fffffffffffffffff'
                                     'fffffffffffffffgggggggggggggggggggggggggg'
                                     'ggggggggggggggggggggggggggggggggggggggggg'
                                     'ggggggggggggggggggggggggggggggggggggggggg'
                                     'ggggggggggggggggggggggggggggggggggggggggg'
                                     'ggggggggggggggggggggggggggggggggggggggggg'
                                     'ggggggggggggggggggggggggggggggggggggggggg'
                                     'ggggggggggggggggggggggggggggggggggggggggg'
                                     'ggggggggggggggggggggggggggggggggggggggggg'
                                     'ggggggggggggggggggggggggggggggggggggggggg'
                                     'ggggggggggggggggggggggggggggggggggggggggg'
                                     'ggggggggggggggggggggggggggggggggggggggggg'
                                     'ggggggggggggggggggggggggggggggggggggggggg'
                                     'gggggggggggggggggggggggggggggggggggbbbbbb'
                                     'bbbbbbbbbbbbbbbbbbbbbbbbbbccccccccccccccc'
                                     'cccccccccccccccccdddddddddddddddddddddddd'
                                     'ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')

    self.assertEqual(icp_bytes, expected_entry_bytes)

    # Tests ICP entry decoding.
    icp_entry = avbtool.AvbIcpEntry(expected_entry_bytes)
    self.assertTrue(icp_entry.is_valid())

    # Tests ICP blob with one entry.
    icp_blob = avbtool.AvbIcpBlob()
    icp_blob.set_algorithm(1)
    icp_blob.add_icp_entry(icp_entry)
    self.assertTrue(icp_blob.is_valid())

    # Now add a 2nd entry (this should fail).
    tl_url2 = 'aftl-test-server.google.ch'
    sth2 = avbtool.AvbIcpSignedRootBlob()
    sth2.leaf_hash = bytearray('f' * 32)
    sth2.tree_size = 4
    sth2.root_hash = bytearray('e' * 32)
    sth2.log_root_sig = bytearray('d' * 512)

    proof_hashes2 = []
    proof_hashes2.append(bytearray('g' * 32))
    proof_hashes2.append(bytearray('h' * 32))
    self.assertTrue(self, self._validate_icp_entry_with_setters(
        tl_url2, 2, sth2, proof_hashes2, 0))

    icp_entry2 = avbtool.AvbIcpEntry()
    icp_entry2.set_log_url(tl_url2)
    icp_entry2.leaf_index = 2
    icp_entry2.set_signed_root_blob(sth2)
    icp_entry2.set_proofs(proof_hashes2)
    icp_entry2.next_entry = 0
    icp_blob.add_icp_entry(icp_entry2)
    self.assertTrue(icp_blob.is_valid())

    # Reset the ICP count to invalidate the entry.
    icp_blob.icp_header.icp_count = 1
    self.assertFalse(icp_blob.is_valid())

    # Fix the entries so this passes.
    icp_blob.icp_header.icp_count = 2
    icp_blob.icp_entries[0].next_entry = 1
    self.assertTrue(icp_blob.is_valid())

    expected_blob_bytes = bytearray(b'AFTL\x00\x00\x00\x01\x00\x00\x00\x01\x00'
                                    '\x00\x00\x01\x00\x02\x00\x00\x00\x1b\x00'
                                    '\x00\x00\x00\x00\x00\x00\x01\x00\x00\x02'
                                    '\x85\x04\x00\x00\x00\x80\x01aftl-test-serv'
                                    'er.google.comaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
                                    'aaa\x00\x00\x00\x00\x00\x00\x00\x02\x00'
                                    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                    'ffffffffffffffffffffffffffffffffgggggggggg'
                                    'gggggggggggggggggggggggggggggggggggggggggg'
                                    'gggggggggggggggggggggggggggggggggggggggggg'
                                    'gggggggggggggggggggggggggggggggggggggggggg'
                                    'gggggggggggggggggggggggggggggggggggggggggg'
                                    'gggggggggggggggggggggggggggggggggggggggggg'
                                    'gggggggggggggggggggggggggggggggggggggggggg'
                                    'gggggggggggggggggggggggggggggggggggggggggg'
                                    'gggggggggggggggggggggggggggggggggggggggggg'
                                    'gggggggggggggggggggggggggggggggggggggggggg'
                                    'gggggggggggggggggggggggggggggggggggggggggg'
                                    'gggggggggggggggggggggggggggggggggggggggggg'
                                    'ggggggggggggggggggggggggggggggggggggggggbb'
                                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbcccccccccccc'
                                    'ccccccccccccccccccccdddddddddddddddddddddd'
                                    'ddddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'
                                    '\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x00'
                                    '\x00\x02\x00\x00\x02\x85\x02\x00\x00\x00@'
                                    '\x00aftl-test-server.google.chffffffffffff'
                                    'ffffffffffffffffffff\x00\x00\x00\x00\x00'
                                    '\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00'
                                    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                                    '\x00\x00\x00\x00eeeeeeeeeeeeeeeeeeeeeeeeee'
                                    'eeeeeedddddddddddddddddddddddddddddddddddd'
                                    'dddddddddddddddddddddddddddddddddddddddddd'
                                    'dddddddddddddddddddddddddddddddddddddddddd'
                                    'dddddddddddddddddddddddddddddddddddddddddd'
                                    'dddddddddddddddddddddddddddddddddddddddddd'
                                    'dddddddddddddddddddddddddddddddddddddddddd'
                                    'dddddddddddddddddddddddddddddddddddddddddd'
                                    'dddddddddddddddddddddddddddddddddddddddddd'
                                    'dddddddddddddddddddddddddddddddddddddddddd'
                                    'dddddddddddddddddddddddddddddddddddddddddd'
                                    'dddddddddddddddddddddddddddddddddddddddddd'
                                    'dddddddddddddddddddddddddddddddddddddddddd'
                                    'ddddddddddddddgggggggggggggggggggggggggggg'
                                    'gggghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')

    self.assertEqual(icp_blob.encode(), expected_blob_bytes)

    icp_blob = avbtool.AvbIcpBlob(expected_blob_bytes)
    self.assertTrue(icp_blob.is_valid())

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
      leaf_hash = avbtool.rfc6962_hash_leaf(leaves[leaf_id])
      root_hash = avbtool.root_from_icp(leaf_id, icp[1], icp[2], leaf_hash)
      self.assertEqual(root_hash, roots[icp[1] -1])

if __name__ == '__main__':
  unittest.main(verbosity=2)

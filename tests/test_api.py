# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Tests for the Akuvox API module."""

from pyakuvox.api import Akuvox


class MockAkuvoxAuth:
    """Mock class for AkuvoxAuth to simulate authentication."""


def test_akuvox_init_sets_auth():
    """Test that the Akuvox API initializes with the provided authentication."""
    mock_auth = MockAkuvoxAuth()
    akuvox = Akuvox(auth=mock_auth)
    assert akuvox.auth is mock_auth

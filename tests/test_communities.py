# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2024 Andrew Grimberg <tykeal@bardicgrove.org>
"""Tests for the Akuvox Communities module."""

from unittest.mock import MagicMock
from pyakuvox.communities import Communities


class DummyAuth:
    """Dummy Auth class for testing Communities."""

    def __init__(self):
        """Initialize the dummy auth with a mock requests method."""
        self.requests = MagicMock()


def test_init_sets_auth():
    """Test that Communities stores the auth instance."""
    auth = DummyAuth()
    communities = Communities(auth)
    assert communities._auth is auth


def test_get_communities_returns_data():
    """Test get_communities returns data from auth.requests."""
    auth = DummyAuth()
    expected_data = [
        {"ID": 1, "Location": "Community1"},
        {"ID": 2, "Location": "Community2"},
    ]
    auth.requests.return_value = {"data": expected_data}
    communities = Communities(auth)
    result = communities.get_communities()
    assert result == expected_data
    auth.requests.assert_called_once_with("GET", "/property/comunityinfo")


def test_get_communities_returns_empty_list_if_no_data():
    """Test get_communities returns empty list if no data key."""
    auth = DummyAuth()
    auth.requests.return_value = {}
    communities = Communities(auth)
    result = communities.get_communities()
    assert result == []

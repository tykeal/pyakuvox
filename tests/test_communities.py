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
    assert len(result) == 2
    assert all(hasattr(c, "ID") and hasattr(c, "Location") for c in result)
    assert result[0].ID == 1
    assert result[0].Location == "Community1"
    auth.requests.assert_called_once_with("GET", "/property/comunityinfo")


def test_get_communities_returns_empty_list_if_no_data():
    """Test get_communities returns empty list if no data key."""
    auth = DummyAuth()
    auth.requests.return_value = {}
    communities = Communities(auth)
    result = communities.get_communities()
    assert result == []


def test_community_get_devices_returns_devices():
    """Test Community.get_devices returns devices from auth.requests."""
    auth = DummyAuth()
    community_data = {"ID": 42, "Location": "TestLoc"}
    expected_devices = [{"id": 1, "name": "Device1"}, {"id": 2, "name": "Device2"}]
    auth.requests.return_value = {"data": expected_devices}
    from pyakuvox.communities import Community

    community = Community(community_data, auth)
    devices = community.get_devices()
    assert devices == expected_devices
    auth.requests.assert_called_once_with(
        "GET", "/property/selectdevice", headers={"x-community-id": "42"}
    )


def test_community_get_devices_returns_empty_list_if_no_devices():
    """Test Community.get_devices returns empty list if no devices key."""
    auth = DummyAuth()
    community_data = {"ID": 99, "Location": "EmptyLoc"}
    auth.requests.return_value = {}
    from pyakuvox.communities import Community

    community = Community(community_data, auth)
    devices = community.get_devices()
    assert devices == {}

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


def test_community_devices_property_returns_devices():
    """Test Community.devices property returns devices from Devices instance."""
    auth = DummyAuth()
    community_data = {"ID": 42, "Location": "TestLoc"}
    from pyakuvox.communities import Community

    community = Community(community_data, auth)
    # The devices property returns the list from the internal Devices instance
    devices = community.devices
    assert (
        devices == []
    )  # Initially empty until get_devices is called on the Devices instance
    assert devices == community._devices.devices


def test_community_has_devices_instance():
    """Test Community initializes with a Devices instance."""
    auth = DummyAuth()
    community_data = {"ID": 99, "Location": "TestLoc"}
    from pyakuvox.communities import Community
    from pyakuvox.devices import Devices

    community = Community(community_data, auth)
    assert isinstance(community._devices, Devices)
    assert community._devices._community_id == 99
    assert community._devices._auth is auth

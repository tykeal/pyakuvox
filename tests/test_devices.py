# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2024 Andrew Grimberg <tykeal@bardicgrove.org>
"""Tests for the Akuvox Devices module."""

from unittest.mock import MagicMock
from pyakuvox.devices import Device, Devices, DEVICE_TYPE


class DummyAuth:
    """Dummy Auth class for testing Devices."""

    def __init__(self):
        """Initialize the dummy auth with a mock requests method."""
        self.requests = MagicMock()


def test_device_init_sets_all_properties():
    """Test that Device properly initializes all properties."""
    device_data = {
        "ID": 123,
        "Relay": "relay1",
        "Location": "Building A",
        "MAC": "00:11:22:33:44:55",
        "Type": "1",
        "Status": 1,
        "UnitName": "Unit 101",
        "RoomName": "Living Room",
        "Name": "Front Door",
        "VersionNumber": "1.2.3",
    }

    device = Device(device_data)

    assert device.ID == "123"
    assert device.Relay == "relay1"
    assert device.Location == "Building A"
    assert device.MAC == "00:11:22:33:44:55"
    assert device.Type == DEVICE_TYPE.DOOR_PHONE
    assert device.Status == 1
    assert device.UnitName == "Unit 101"
    assert device.RoomName == "Living Room"
    assert device.Name == "Front Door"
    assert device.VersionNumber == "1.2.3"


def test_device_init_with_missing_data():
    """Test Device initialization with missing data."""
    device_data = {}

    device = Device(device_data)

    assert device.ID == ""
    assert device.Relay == ""
    assert device.Location == ""
    assert device.MAC == ""
    assert device.Type == DEVICE_TYPE.STAIR_PHONE  # Default type
    assert device.Status == 0
    assert device.UnitName == ""
    assert device.RoomName == ""
    assert device.Name == ""
    assert device.VersionNumber == ""


def test_devices_init_sets_auth():
    """Test that Devices stores the auth instance."""
    auth = DummyAuth()
    devices = Devices("1", auth)
    assert devices._auth is auth
    assert devices._community_id == "1"
    assert devices._devices == []


def test_devices_property_returns_device_list():
    """Test that devices property returns the device list."""
    auth = DummyAuth()
    devices = Devices("1", auth)
    assert devices.devices == []
    assert devices.devices is devices._devices


def test_devices_get_devices_populates_device_list():
    """Test that get_devices populates the device list from API."""
    auth = DummyAuth()
    devices = Devices("123", auth)

    api_response = {
        "data": {
            "row": [
                {
                    "ID": 1,
                    "Name": "Front Door",
                    "MAC": "00:11:22:33:44:55",
                    "Type": "1",
                    "Status": 1,
                },
                {
                    "ID": 2,
                    "Name": "Back Door",
                    "MAC": "00:11:22:33:44:66",
                    "Type": "1",
                    "Status": 0,
                },
            ]
        }
    }
    auth.requests.return_value = api_response

    devices.get_devices()

    assert len(devices.devices) == 2
    assert devices.devices[0].ID == "1"
    assert devices.devices[0].Name == "Front Door"
    assert devices.devices[0].MAC == "00:11:22:33:44:55"
    assert devices.devices[1].ID == "2"
    assert devices.devices[1].Name == "Back Door"
    assert devices.devices[1].MAC == "00:11:22:33:44:66"

    auth.requests.assert_called_once_with(
        "GET", "/property/selectdevice", headers={"x-community-id": "123"}
    )


def test_devices_get_devices_handles_missing_data_key():
    """Test that get_devices handles response without data key."""
    auth = DummyAuth()
    devices = Devices("456", auth)

    auth.requests.return_value = {}

    devices.get_devices()

    assert len(devices.devices) == 0
    auth.requests.assert_called_once_with(
        "GET", "/property/selectdevice", headers={"x-community-id": "456"}
    )


def test_devices_get_devices_handles_missing_row_key():
    """Test that get_devices handles response without row key in data."""
    auth = DummyAuth()
    devices = Devices("789", auth)

    auth.requests.return_value = {"data": {}}

    devices.get_devices()

    assert len(devices.devices) == 0


def test_devices_get_devices_clears_existing_devices():
    """Test that get_devices clears existing devices before populating."""
    auth = DummyAuth()
    devices = Devices("111", auth)

    # First call
    auth.requests.return_value = {"data": {"row": [{"ID": 1, "Name": "Device1"}]}}
    devices.get_devices()
    assert len(devices.devices) == 1

    # Second call with different data
    auth.requests.return_value = {
        "data": {"row": [{"ID": 2, "Name": "Device2"}, {"ID": 3, "Name": "Device3"}]}
    }
    devices.get_devices()

    assert len(devices.devices) == 2
    assert devices.devices[0].ID == "2"
    assert devices.devices[1].ID == "3"


def test_devices_get_devices_handles_empty_row():
    """Test that get_devices handles empty row list."""
    auth = DummyAuth()
    devices = Devices("222", auth)

    auth.requests.return_value = {"data": {"row": []}}

    devices.get_devices()

    assert len(devices.devices) == 0

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2024 Andrew Grimberg <tykeal@bardicgrove.org>
"""Tests for the Akuvox Devices module."""

from unittest.mock import MagicMock
from pyakuvox.devices import Device, Devices, DEVICE_TYPE, DEVICE_STATUS


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
        "Status": "1",
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
    assert device.Status == DEVICE_STATUS.ONLINE
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
    assert device.Status == DEVICE_STATUS.OFFLINE  # Default status
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
                    "Status": "1",
                },
                {
                    "ID": 2,
                    "Name": "Back Door",
                    "MAC": "00:11:22:33:44:66",
                    "Type": "1",
                    "Status": "0",
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

    # Access through property which will call get_devices() once
    assert len(devices.devices) == 0
    auth.requests.assert_called_once_with(
        "GET", "/property/selectdevice", headers={"x-community-id": "456"}
    )


def test_devices_get_devices_handles_missing_row_key():
    """Test that get_devices handles response without row key in data."""
    auth = DummyAuth()
    devices = Devices("789", auth)

    auth.requests.return_value = {"data": {}}

    # Access through property which will call get_devices() once
    assert len(devices.devices) == 0


def test_devices_get_devices_clears_existing_devices():
    """Test that get_devices clears existing devices before populating."""
    auth = DummyAuth()
    devices = Devices("111", auth)

    # First call
    auth.requests.return_value = {"data": {"row": [{"ID": 1, "Name": "Device1"}]}}
    devices.get_devices()
    assert len(devices._devices) == 1

    # Second call with different data
    auth.requests.return_value = {
        "data": {"row": [{"ID": 2, "Name": "Device2"}, {"ID": 3, "Name": "Device3"}]}
    }
    devices.get_devices()

    assert len(devices._devices) == 2
    assert devices._devices[0].ID == "2"
    assert devices._devices[1].ID == "3"


def test_devices_get_devices_handles_empty_row():
    """Test that get_devices handles empty row list."""
    auth = DummyAuth()
    devices = Devices("222", auth)

    auth.requests.return_value = {"data": {"row": []}}

    # Access through property which will call get_devices() once
    assert len(devices.devices) == 0


def test_devices_get_devices_by_type():
    """Test that get_devices_by_type filters devices correctly."""
    auth = DummyAuth()
    devices = Devices("333", auth)

    api_response = {
        "data": {
            "row": [
                {"ID": 1, "Name": "Door1", "Type": "1"},  # DOOR_PHONE
                {"ID": 2, "Name": "Monitor1", "Type": "2"},  # INDOOR_MONITOR
                {"ID": 3, "Name": "Door2", "Type": "1"},  # DOOR_PHONE
                {"ID": 4, "Name": "Stair1", "Type": "0"},  # STAIR_PHONE
            ]
        }
    }
    auth.requests.return_value = api_response

    door_phones = devices.get_devices_by_type(DEVICE_TYPE.DOOR_PHONE)
    assert len(door_phones) == 2
    assert door_phones[0].Name == "Door1"
    assert door_phones[1].Name == "Door2"

    indoor_monitors = devices.get_devices_by_type(DEVICE_TYPE.INDOOR_MONITOR)
    assert len(indoor_monitors) == 1
    assert indoor_monitors[0].Name == "Monitor1"

    stair_phones = devices.get_devices_by_type(DEVICE_TYPE.STAIR_PHONE)
    assert len(stair_phones) == 1
    assert stair_phones[0].Name == "Stair1"


def test_devices_type_properties():
    """Test that device type properties return filtered devices."""
    auth = DummyAuth()
    devices = Devices("444", auth)

    api_response = {
        "data": {
            "row": [
                {"ID": 1, "Name": "Door1", "Type": "1"},
                {"ID": 2, "Name": "Monitor1", "Type": "2"},
                {"ID": 3, "Name": "Stair1", "Type": "0"},
                {"ID": 5, "Name": "Door2", "Type": "1"},
            ]
        }
    }
    auth.requests.return_value = api_response

    # Test door_phones property
    door_phones = devices.door_phones
    assert len(door_phones) == 2
    assert all(d.Type == DEVICE_TYPE.DOOR_PHONE for d in door_phones)

    # Test indoor_monitors property
    indoor_monitors = devices.indoor_monitors
    assert len(indoor_monitors) == 1
    assert all(d.Type == DEVICE_TYPE.INDOOR_MONITOR for d in indoor_monitors)

    # Test stair_phones property
    stair_phones = devices.stair_phones
    assert len(stair_phones) == 1
    assert all(d.Type == DEVICE_TYPE.STAIR_PHONE for d in stair_phones)

    # Verify API was only called once (due to lazy loading)
    auth.requests.assert_called_once()


def test_devices_type_properties_with_no_devices():
    """Test that device type properties return empty lists when no devices exist."""
    auth = DummyAuth()
    devices = Devices("555", auth)

    auth.requests.return_value = {"data": {"row": []}}

    assert devices.door_phones == []
    assert devices.indoor_monitors == []
    assert devices.stair_phones == []

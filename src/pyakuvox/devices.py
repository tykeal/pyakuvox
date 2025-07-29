# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Andrew Grimberg <tykeal@bardicgrove.org>
"""Devices management for the Akuvox system."""

from __future__ import annotations

from enum import StrEnum

from .auth import Auth


class DEVICE_TYPE(StrEnum):
    """Device type enumeration."""

    # Add device types as needed
    STAIR_PHONE = "0"
    DOOR_PHONE = "1"
    INDOOR_MONITOR = "2"
    # Add more types as discovered


class Device:
    """Represents a single device."""

    def __init__(self, data: dict) -> None:
        """Initialize the Device instance.

        :param data: The device data dictionary.
        :type data: dict
        """
        self.ID: str = str(data.get("ID", ""))
        self.Relay: str = str(data.get("Relay", ""))
        self.Location: str = data.get("Location", "")
        self.MAC: str = data.get("MAC", "")
        self.Type: DEVICE_TYPE = DEVICE_TYPE(data.get("Type", "0"))
        self.Status: int = data.get("Status", 0)
        self.UnitName: str = data.get("UnitName", "")
        self.RoomName: str = data.get("RoomName", "")
        self.Name: str = data.get("Name", "")
        self.VersionNumber: str = data.get("VersionNumber", "")


class Devices:
    """Devices management for the Akuvox system."""

    def __init__(self, community_id: str, auth: Auth) -> None:
        """Initialize the Devices manager.

        :param auth: An instance of the Auth class for authentication.
        :type auth: Auth
        """
        self._auth = auth
        self._community_id: str = community_id
        self._devices: list[Device] = []

    @property
    def devices(self) -> list[Device]:
        """Return the list of devices."""
        if not self._devices:
            self.get_devices()
        return self._devices

    def get_devices(self) -> None:
        """Retrieve the list of devices in the community.

        :return: A list of Device instances.
        :rtype: list[Device]
        """
        path = "/property/selectdevice"
        headers = {"x-community-id": str(self._community_id)}
        response = self._auth.requests("GET", path, headers=headers)
        data = response.get("data", {})
        if "row" in data:
            data = data["row"]
            self._devices = [Device(item) for item in data]

    def get_devices_by_type(self, device_type: DEVICE_TYPE) -> list[Device]:
        """Return devices filtered by type.

        :param device_type: The device type to filter by.
        :type device_type: DEVICE_TYPE
        :return: A list of Device instances of the specified type.
        :rtype: list[Device]
        """
        if not self._devices:
            self.get_devices()
        return [device for device in self._devices if device.Type == device_type]

    @property
    def door_phones(self) -> list[Device]:
        """Return all door phone devices."""
        return self.get_devices_by_type(DEVICE_TYPE.DOOR_PHONE)

    @property
    def indoor_monitors(self) -> list[Device]:
        """Return all indoor monitor devices."""
        return self.get_devices_by_type(DEVICE_TYPE.INDOOR_MONITOR)

    @property
    def stair_phones(self) -> list[Device]:
        """Return all stair phone devices."""
        return self.get_devices_by_type(DEVICE_TYPE.STAIR_PHONE)

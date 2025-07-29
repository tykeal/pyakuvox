# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Andrew Grimberg <tykeal@bardicgrove.org>
"""Communities management for the Akuvox system."""

from __future__ import annotations
from typing import Any

from .auth import Auth
from .devices import Device, Devices


class Community:
    """Represents a single community."""

    def __init__(self, data: dict[str, Any], auth: Auth) -> None:
        """Initialize the Community instance.

        :param data: The community data dictionary.
        :type data: dict
        :param auth: An instance of the Auth class for authentication.
        :type auth: Auth
        """
        self.ID = data.get("ID", "")
        self.Location = data.get("Location", "")
        self._auth = auth
        self._devices = Devices(self.ID, self._auth)

    @property
    def devices(self) -> list[Device]:
        """Return the list of devices in this community.

        :return: A list of Device instances.
        :rtype: list[Device]
        """
        return self._devices.devices


class Communities:
    """Communities management for the Akuvox system."""

    def __init__(self, auth: Auth) -> None:
        """Initialize the Communities manager.

        :param auth: An instance of the Auth class for authentication.
        :type auth: Auth
        """
        self._auth = auth

    def get_communities(self) -> list[Community]:
        """Retrieve a list of communities.

        :return: A list of communities.
        :rtype: list[dict]
        """
        path = "/property/comunityinfo"
        response = self._auth.requests("GET", path)
        data = response.get("data", [])
        return [Community(item, self._auth) for item in data]

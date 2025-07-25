# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Communities management for the Akuvox system."""

from __future__ import annotations

from .auth import Auth


class Community:
    """Represents a single community."""

    def __init__(self, data, auth) -> None:
        """Initialize the Community instance.

        :param data: The community data dictionary.
        :type data: dict
        :param auth: An instance of the Auth class for authentication.
        :type auth: Auth
        """
        self.ID = data.get("ID")
        self.Location = data.get("Location")
        self._auth = auth

    def get_devices(self) -> dict:
        """Return the list of devices in this community."""
        path = "/property/selectdevice"
        headers = {"x-community-id": str(self.ID)}
        response = self._auth.requests("GET", path, headers=headers)
        return response.get("data", {})


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

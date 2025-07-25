# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Communities management for the Akuvox system."""

from __future__ import annotations

from .auth import Auth


class Communities:
    """Communities management for the Akuvox system."""

    def __init__(self, auth: Auth) -> None:
        """Initialize the Communities manager.

        :param auth: An instance of the Auth class for authentication.
        :type auth: Auth
        """
        self._auth = auth

    def get_communities(self) -> list[dict]:
        """Retrieve a list of communities.

        :return: A list of communities.
        :rtype: list[dict]
        """
        path = "/property/comunityinfo"
        response = self._auth.requests("GET", path)
        return response.get("data", [])

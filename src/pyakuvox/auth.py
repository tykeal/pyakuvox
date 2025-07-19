# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Authentication and session management for the Akuvox system."""

from __future__ import annotations
from typing import Final

import requests

from .const import BASE_DOMAIN
from .const import SUBDOMAINS_LIST
from .exceptions import NotAuthenticatedError


class AkuvoxAuth:
    """Class to handle authentication and session management for Akuvox."""

    def __init__(self, subdomain: str, username: str, password: str) -> None:
        """Initialize the AkuvoxAuth with a specific subdomain.

        :param subdomain: The subdomain to use for the Akuvox API.
        :type subdomain: str
        :param username: The username for authentication.
        :type username: str
        :param password: The password for authentication.
        :type password: str
        """
        if subdomain not in SUBDOMAINS_LIST:
            raise ValueError(
                f"Invalid subdomain: {subdomain}. Must be one of {SUBDOMAINS_LIST}."
            )
        self.base_url: Final[str] = f"https://api.{subdomain}.{BASE_DOMAIN}"
        self.username: Final[str] = username
        self.password: Final[str] = password

        self._token: str | None = None
        self._grade: str | None = None
        self._account: str | None = None
        self._timezone: str | None = None
        self._community_id: str | None = None
        self._role: str | None = None

    def authenticate(self) -> None:
        """Authenticate the user with the provided credentials."""
        url = f"{self.base_url}/property/login"

        payload = {
            "Account": self.username,
            "passwd": self.password,
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        if "response" in data and data["response"] == "0":
            pass
        else:
            raise NotAuthenticatedError(
                f"Authentication failed: {data.get('message', 'Unknown error')}"
            )

        if "token" in data:
            self._token = data["token"]
        else:
            raise NotAuthenticatedError("Authentication failed: No token received.")

        if "grade" in data:
            self._grade = data["grade"]

        if "account" in data:
            self._account = data["account"]

        if "timezone" in data:
            self._timezone = data["timezone"]

        if "community_id" in data:
            self._community_id = data["community_id"]

        if "role" in data:
            self._role = data["role"]

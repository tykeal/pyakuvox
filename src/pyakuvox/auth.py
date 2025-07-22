# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Authentication and session management for the Akuvox system."""

from __future__ import annotations
from typing import Final

import requests

from .const import BASE_DOMAIN
from .const import DEFAULT_TIMEOUT
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

        response = requests.post(
            url, json=payload, timeout=DEFAULT_TIMEOUT, verify=True
        )
        response.raise_for_status()
        data = response.json()
        if not ("response" in data and data["response"] == "0"):
            raise NotAuthenticatedError(
                f"Authentication failed: {data.get('message', 'Unknown error')}"
            )

        key_to_attr = {
            "token": "_token",
            "grade": "_grade",
            "account": "_account",
            "timezone": "_timezone",
            "community_id": "_community_id",
            "role": "_role",
        }

        for key, attr in key_to_attr.items():
            if key in data:
                setattr(self, attr, data[key])

    @property
    def token(self) -> str:
        """Get the authentication token.

        :raises NotAuthenticatedError: If the user is not authenticated.
        """
        if self._token is None:
            raise NotAuthenticatedError("User is not authenticated.")
        return self._token

    @property
    def grade(self) -> str | None:
        """Get the user's grade."""
        return self._grade

    @property
    def account(self) -> str | None:
        """Get the user's account."""
        return self._account

    @property
    def timezone(self) -> str | None:
        """Get the user's timezone."""
        return self._timezone

    @property
    def community_id(self) -> str | None:
        """Get the user's community ID."""
        return self._community_id

    @property
    def role(self) -> str | None:
        """Get the user's role."""
        return self._role

    def is_authenticated(self) -> bool:
        """Check if the user is authenticated.

        :return: True if authenticated, False otherwise.
        :rtype: bool
        """
        return self._token is not None

    def __repr__(self) -> str:
        """Return a string representation of the AkuvoxAuth object."""
        return f"AkuvoxAuth(subdomain={self.base_url}, username=[REDACTED])"

    def __str__(self) -> str:
        """Return a user-friendly string representation of the AkuvoxAuth object."""
        return self.__repr__()

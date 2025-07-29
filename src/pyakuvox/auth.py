# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Andrew Grimberg <tykeal@bardicgrove.org>
"""Authentication and session management for the Akuvox system."""

from __future__ import annotations
from typing import Final

import requests

from .const import BASE_DOMAIN
from .const import DEFAULT_TIMEOUT
from .const import RESULTS
from .const import RESULT_INVALID_USERNAME_OR_PASSWORD
from .const import RESULT_SUCCESS
from .const import RESULT_UNKNOWN
from .const import SUBDOMAINS_LIST
from .exceptions import NotAuthenticatedError, UnknownError


def _raise_for_result(result: int, message: str | None = None) -> None:
    """Raise an exception based on the result code.

    :param result: The result code from the API response.
    :type result: int
    :param message: Optional message to include in the exception.
    :type message: str | None
    :raises UnknownError: If the result code indicates an error.

    :meta private:
    """
    if result in RESULTS:
        if result != RESULT_SUCCESS:
            error_message = message or RESULTS[result]
            if result == RESULT_INVALID_USERNAME_OR_PASSWORD:
                raise NotAuthenticatedError(error_message)
            else:
                raise UnknownError(
                    f"API request failed with result {result}: {error_message}"
                )


def _requests(method: str, url: str, **kwargs) -> dict:
    """Make a request to the Akuvox API.

    :param method: HTTP method to use (e.g., 'GET', 'POST').
    :type method: str
    :param url: The URL to send the request to.
    :type url: str
    :param kwargs: Additional keyword arguments for the request.
    :return: The parsed JSON response from the Akuvox API.
    :rtype: dict

    :meta private:
    """
    try:
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        kwargs.setdefault("verify", True)  # Ensure SSL verification is enabled
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()

        json_response = response.json()
        _raise_for_result(
            json_response.get("result", RESULT_UNKNOWN), json_response.get("message")
        )

        return json_response
    except requests.RequestException as e:
        raise UnknownError(f"Request failed: {e}")


class Auth:
    """Class to handle authentication and session management for Akuvox."""

    def __init__(self, subdomain: str, username: str, password: str) -> None:
        """Initialize the Auth with a specific subdomain.

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

        data = _requests("POST", url, json=payload)

        key_to_attr = {
            "token": "_token",
            "grade": "_grade",
            "account": "_account",
            "timeZone": "_timezone",
            "communityID": "_community_id",
            "Role": "_role",
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

    @property
    def is_authenticated(self) -> bool:
        """Check if the user is authenticated.

        :return: True if authenticated, False otherwise.
        :rtype: bool
        """
        return self._token is not None

    def __repr__(self) -> str:
        """Return a string representation of the Auth object."""
        return f"Auth(subdomain={self.base_url}, username=[REDACTED])"

    def __str__(self) -> str:
        """Return a user-friendly string representation of the Auth object."""
        return self.__repr__()

    def requests(self, method: str, path: str, **kwargs) -> dict:
        """Make a request to the Akuvox API using the authenticated session.

        :param method: HTTP method to use (e.g., 'GET', 'POST').
        :type method: str
        :param path: The API endpoint to send the request to.
        :type path: str
        :param kwargs: Additional keyword arguments for the request.
        :return: The response from the Akuvox API.
        :rtype: dict
        """
        if not self.is_authenticated:
            self.authenticate()

        url = f"{self.base_url}/{path.lstrip('/')}"
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["x-auth-token"] = self.token

        return _requests(method, url, **kwargs)

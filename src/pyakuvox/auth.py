# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Authentication and session management for the Akuvox system."""

from __future__ import annotations
from typing import Final

from .const import BASE_DOMAIN
from .const import SUBDOMAINS_LIST


class AkuvoxAuth:
    """Class to handle authentication and session management for Akuvox."""

    def __init__(self, subdomain: str) -> None:
        """Initialize the AkuvoxAuth with a specific subdomain."""
        if subdomain not in SUBDOMAINS_LIST:
            raise ValueError(
                f"Invalid subdomain: {subdomain}. Must be one of {SUBDOMAINS_LIST}."
            )
        self.base_url: Final[str] = f"https://api.{subdomain}.{BASE_DOMAIN}"

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate the user with the provided credentials."""
        # Placeholder for actual authentication logic
        return True  # Assume authentication is successful for now

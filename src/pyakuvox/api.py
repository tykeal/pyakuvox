# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""API for interacting with Akuvox services."""

from __future__ import annotations

from .auth import Auth


class Akuvox:
    """API for interacting with Akuvox services."""

    def __init__(self, auth: Auth) -> None:
        """Initialize the Akuvox API with authentication.

        :param auth: An instance of Auth for authentication.
        :type auth: Auth
        """
        self.auth = auth

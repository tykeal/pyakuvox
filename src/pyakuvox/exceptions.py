# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Exceptions for the pyakuvox library."""


class AkuvoxError(Exception):
    """Base class for all Akuvox exceptions."""


class NotAuthenticatedError(AkuvoxError):
    """Exception raised when a user is not authenticated."""

    def __init__(self, message: str = "User is not authenticated."):
        """Raise an error when a user is not authenticated."""
        super().__init__(message)

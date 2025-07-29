# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Andrew Grimberg <tykeal@bardicgrove.org>
"""Exceptions for the pyakuvox library."""


class AkuvoxError(Exception):
    """Base class for all Akuvox exceptions."""


class NotAuthenticatedError(AkuvoxError):
    """Exception raised when a user is not authenticated."""

    def __init__(self, message: str = "User is not authenticated."):
        """Raise an error when a user is not authenticated."""
        super().__init__(message)


class UnknownError(AkuvoxError):
    """Exception raised for unknown errors."""

    def __init__(self, message: str = "An unknown error occurred."):
        """Raise an error when an unknown error occurs."""
        super().__init__(message)

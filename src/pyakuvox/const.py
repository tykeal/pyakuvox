# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Andrew Grimberg <tykeal@bardicgrove.org>
"""Constants for the pyakuvox library."""

from __future__ import annotations
from typing import Final

BASE_DOMAIN: Final[str] = "akuvox.com"

DEFAULT_TIMEOUT: Final[int] = 60

SUBDOMAIN_AMERICA: Final[str] = "ucloud"
SUBDOMAIN_ASIA: Final[str] = "scloud"
SUBDOMAIN_CHINA: Final[str] = "ccloud"
SUBDOMAIN_EU: Final[str] = "ecloud"
SUBDOMAIN_TEST: Final[str] = "dev39"

SUBDOMAINS_LIST: Final[list[str]] = [
    SUBDOMAIN_AMERICA,
    SUBDOMAIN_ASIA,
    SUBDOMAIN_CHINA,
    SUBDOMAIN_EU,
    SUBDOMAIN_TEST,
]

# Result codes
RESULT_UNKNOWN: Final[int] = -1
RESULT_SUCCESS: Final[int] = 0
RESULT_INVALID_USERNAME_OR_PASSWORD: Final[int] = 3
RESULT_INVALID_IDENTITY: Final[int] = 1006

RESULTS: Final[dict[int, str]] = {
    RESULT_UNKNOWN: "Unknown error",
    RESULT_SUCCESS: "Success",
    RESULT_INVALID_USERNAME_OR_PASSWORD: "Invalid username or password",
    RESULT_INVALID_IDENTITY: "Invalid identity",
}

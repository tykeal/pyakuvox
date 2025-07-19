# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Constants for the pyakuvox library."""

from __future__ import annotations
from typing import Final

BASE_DOMAIN: Final[str] = "akuvox.com"

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

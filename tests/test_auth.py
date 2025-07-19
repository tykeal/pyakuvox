# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Tests for the Akuvox authentication module."""

import pytest
from pyakuvox.auth import AkuvoxAuth
from pyakuvox.const import SUBDOMAINS_LIST, BASE_DOMAIN


def test_init_valid_subdomain():
    """Test initialization with a valid subdomain."""
    subdomain = SUBDOMAINS_LIST[0]
    auth = AkuvoxAuth(subdomain)
    assert auth.base_url == f"https://api.{subdomain}.{BASE_DOMAIN}"


def test_init_invalid_subdomain():
    """Test initialization with an invalid subdomain."""
    invalid_subdomain = "invalid"
    with pytest.raises(ValueError) as excinfo:
        AkuvoxAuth(invalid_subdomain)
    assert "Invalid subdomain" in str(excinfo.value)


def test_authenticate_returns_true():
    """Test that authenticate method returns True for valid credentials."""
    subdomain = SUBDOMAINS_LIST[0]
    auth = AkuvoxAuth(subdomain)
    assert auth.authenticate("user", "pass") is True


def test_repr_and_str():
    """Test that repr and str methods do not raise and contain class name."""
    subdomain = SUBDOMAINS_LIST[0]
    auth = AkuvoxAuth(subdomain)
    # Check that repr and str do not raise and contain class name
    assert "AkuvoxAuth" in repr(auth)
    assert "AkuvoxAuth" in str(auth)

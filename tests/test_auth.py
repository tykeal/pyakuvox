# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Tests for the Akuvox authentication module."""

import pytest
from unittest.mock import patch, MagicMock
from pyakuvox.auth import AkuvoxAuth
from pyakuvox.const import SUBDOMAINS_LIST, BASE_DOMAIN


def test_init_valid_subdomain():
    """Test initialization with a valid subdomain."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = AkuvoxAuth(subdomain, username, password)
    assert auth.base_url == f"https://api.{subdomain}.{BASE_DOMAIN}"
    assert auth.username == username
    assert auth.password == password
    assert auth._token is None


def test_init_invalid_subdomain():
    """Test initialization with an invalid subdomain."""
    invalid_subdomain = "invalid"
    username = "user"
    password = "pass"
    with pytest.raises(ValueError) as excinfo:
        AkuvoxAuth(invalid_subdomain, username, password)
    assert "Invalid subdomain" in str(excinfo.value)


@patch("pyakuvox.auth.requests.post")
def test_authenticate_success(mock_post):
    """Test successful authentication."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = AkuvoxAuth(subdomain, username, password)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "0", "token": "fake-token"}
    mock_post.return_value = mock_response

    auth.authenticate()
    assert auth._token == "fake-token"
    mock_post.assert_called_once()


@patch("pyakuvox.auth.requests.post")
def test_authenticate_failure(mock_post):
    """Test authentication failure."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = AkuvoxAuth(subdomain, username, password)

    mock_response = MagicMock()
    # Akuvox API returns 200 response for all authentication
    # There is a "response" field in the JSON that indicates success or failure.
    mock_response.status_code = 200
    mock_response.json.return_value = {"error": "Unauthorized"}
    mock_post.return_value = mock_response

    with pytest.raises(Exception) as excinfo:
        auth.authenticate()
    assert "Authentication failed" in str(excinfo.value)
    assert auth._token is None


def test_repr_and_str():
    """Test that repr and str methods do not raise and contain class name."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = AkuvoxAuth(subdomain, username, password)
    assert "AkuvoxAuth" in repr(auth)
    assert "AkuvoxAuth" in str(auth)

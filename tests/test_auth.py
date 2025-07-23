# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Tests for the Akuvox authentication module."""

import pytest
from unittest.mock import patch, MagicMock
from pyakuvox.auth import AkuvoxAuth
from pyakuvox.const import SUBDOMAINS_LIST, BASE_DOMAIN
from pyakuvox.exceptions import NotAuthenticatedError


def test_init_valid_subdomain():
    """Test initialization with a valid subdomain."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = AkuvoxAuth(subdomain, username, password)
    assert auth.base_url == f"https://api.{subdomain}.{BASE_DOMAIN}"
    assert auth.username == username
    assert auth.password == password
    with pytest.raises(NotAuthenticatedError) as excinfo:
        auth.token
    assert "User is not authenticated" in str(excinfo.value)
    assert auth.is_authenticated() is False


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
    mock_response.json.return_value = {
        "result": "0",
        "token": "fake-token",
        "grade": "user",
        "account": "user_account",
        "timezone": "UTC",
        "community_id": "community_123",
        "role": "user_role",
    }
    mock_post.return_value = mock_response

    auth.authenticate()
    assert auth.token == "fake-token"
    assert auth.grade == "user"
    assert auth.account == "user_account"
    assert auth.timezone == "UTC"
    assert auth.community_id == "community_123"
    assert auth.role == "user_role"
    assert auth.is_authenticated() is True
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

    with pytest.raises(NotAuthenticatedError) as excinfo:
        auth.authenticate()
    assert "Authentication failed" in str(excinfo.value)
    with pytest.raises(NotAuthenticatedError) as excinfo:
        auth.token
    assert "User is not authenticated" in str(excinfo.value)
    assert auth.is_authenticated() is False


def test_repr_and_str():
    """Test that repr and str methods do not raise and contain class name."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = AkuvoxAuth(subdomain, username, password)
    assert "AkuvoxAuth" in repr(auth)
    assert "AkuvoxAuth" in str(auth)

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2023 Andrew Grimberg <tykeal@bardicgrove.org>
"""Tests for the Akuvox authentication module."""

import pytest
from unittest.mock import patch, MagicMock
from pyakuvox.auth import Auth
from pyakuvox.const import SUBDOMAINS_LIST, BASE_DOMAIN
from pyakuvox.const import RESULT_SUCCESS, RESULT_INVALID_USERNAME_OR_PASSWORD
from pyakuvox.exceptions import NotAuthenticatedError, UnknownError


def test_init_valid_subdomain():
    """Test initialization with a valid subdomain."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = Auth(subdomain, username, password)
    assert auth.base_url == f"https://api.{subdomain}.{BASE_DOMAIN}"
    assert auth.username == username
    assert auth.password == password
    with pytest.raises(NotAuthenticatedError) as excinfo:
        auth.token
    assert "User is not authenticated" in str(excinfo.value)
    assert auth.is_authenticated is False


def test_init_invalid_subdomain():
    """Test initialization with an invalid subdomain."""
    invalid_subdomain = "invalid"
    username = "user"
    password = "pass"
    with pytest.raises(ValueError) as excinfo:
        Auth(invalid_subdomain, username, password)
    assert "Invalid subdomain" in str(excinfo.value)


@patch("pyakuvox.auth.requests.request")
def test_authenticate_success(mock_post):
    """Test successful authentication."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = Auth(subdomain, username, password)

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": RESULT_SUCCESS,
        "token": "fake-token",
        "grade": "user",
        "account": "user_account",
        "timeZone": "UTC",
        "communityID": "community_123",
        "Role": "user_role",
    }
    mock_post.return_value = mock_response

    auth.authenticate()
    assert auth.token == "fake-token"
    assert auth.grade == "user"
    assert auth.account == "user_account"
    assert auth.timezone == "UTC"
    assert auth.community_id == "community_123"
    assert auth.role == "user_role"
    assert auth.is_authenticated is True
    mock_post.assert_called_once()


@patch("pyakuvox.auth.requests.request")
def test_authenticate_failure(mock_post):
    """Test authentication failure."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = Auth(subdomain, username, password)

    mock_response = MagicMock()
    # Akuvox API returns 200 response for all authentication
    # There is a "response" field in the JSON that indicates success or failure.
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": RESULT_INVALID_USERNAME_OR_PASSWORD,
        "message": "Unauthorized",
    }
    mock_post.return_value = mock_response

    with pytest.raises(NotAuthenticatedError) as excinfo:
        auth.authenticate()
    assert "Unauthorized" in str(excinfo.value)
    with pytest.raises(NotAuthenticatedError) as excinfo:
        auth.token
    assert "User is not authenticated" in str(excinfo.value)
    assert auth.is_authenticated is False


def test_repr_and_str():
    """Test that repr and str methods do not raise and contain class name."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = Auth(subdomain, username, password)
    assert "Auth" in repr(auth)
    assert "Auth" in str(auth)


def test__raise_for_result_success():
    """Test _raise_for_result with a successful result code."""
    from pyakuvox.auth import _raise_for_result

    # Should not raise for RESULT_SUCCESS
    _raise_for_result(RESULT_SUCCESS)


def test__raise_for_result_failure():
    """Test _raise_for_result raises UnknownError for error result."""
    from pyakuvox.auth import _raise_for_result

    with pytest.raises(NotAuthenticatedError) as excinfo:
        _raise_for_result(RESULT_INVALID_USERNAME_OR_PASSWORD)
    assert "Invalid username or password" in str(excinfo.value)


def test__raise_for_result_unknown():
    """Test _raise_for_result raises UnknownError for error result."""
    from pyakuvox.auth import _raise_for_result
    from pyakuvox.const import RESULT_UNKNOWN

    with pytest.raises(UnknownError) as excinfo:
        _raise_for_result(RESULT_UNKNOWN)
    assert "Unknown error" in str(excinfo.value)


@patch("pyakuvox.auth.requests.request")
def test__requests_success(mock_request):
    """Test _requests returns JSON and calls _raise_for_result."""
    from pyakuvox.auth import _requests

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "result": RESULT_SUCCESS,
        "message": "Success",
        "foo": "bar",
    }
    mock_request.return_value = mock_response
    result = _requests("POST", "http://test", json={"foo": "bar"})
    assert result["foo"] == "bar"
    mock_request.assert_called_once()


@patch("pyakuvox.auth.requests.request")
def test__requests_failure(mock_request):
    """Test _requests raises UnknownError on request exception."""
    from pyakuvox.auth import _requests
    from requests import RequestException

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "result": RESULT_SUCCESS,
        "message": "Success",
        "foo": "bar",
    }
    mock_request.return_value = mock_response
    mock_request.side_effect = RequestException("Connection error")
    with pytest.raises(UnknownError) as excinfo:
        _requests("POST", "http://test", json={})
    assert "Request failed" in str(excinfo.value)


@patch("pyakuvox.auth._requests")
@patch.object(Auth, "is_authenticated", return_value=True)
def test_auth_requests_success(mock_is_authenticated, mock__requests):
    """Test Auth.requests returns JSON on success and passes correct arguments."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = Auth(subdomain, username, password)
    auth._token = "fake-token"
    mock__requests.return_value = {"result": RESULT_SUCCESS, "message": "Success"}
    result = auth.requests("POST", "/test", json={"foo": "bar"})
    assert result["message"] == "Success"
    mock__requests.assert_called_once()
    args, kwargs = mock__requests.call_args
    assert args[0] == "POST"
    assert "/test" in args[1]
    assert kwargs["headers"]["x-auth-token"] == "fake-token"


@patch("pyakuvox.auth._requests")
@patch.object(Auth, "authenticate")
def test_auth_requests_triggers_authenticate(mock_authenticate, mock__requests):
    """Test Auth.requests calls authenticate if not authenticated."""
    subdomain = SUBDOMAINS_LIST[0]
    username = "user"
    password = "pass"
    auth = Auth(subdomain, username, password)
    mock__requests.return_value = {"result": RESULT_SUCCESS, "message": "Success"}
    with pytest.raises(NotAuthenticatedError):
        auth.requests("POST", "/test", json={"foo": "bar"})
    mock_authenticate.assert_called_once()

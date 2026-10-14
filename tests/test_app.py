import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import app as portal  # noqa: E402
import config  # noqa: E402


@pytest.fixture
def client():
    portal.app.config["TESTING"] = True
    return portal.app.test_client()


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthy"


def test_index_renders(client):
    assert client.get("/").status_code == 200


def test_tokens_page_never_leaks_values(client, monkeypatch):
    secret = "super-secret-token-value"
    monkeypatch.setattr(portal, "WINDY_API_TOKEN", secret)
    monkeypatch.setattr(portal, "WINDY_API_TOKEN_MAP", secret)
    monkeypatch.setattr(portal, "WINDY_API_TOKEN_POINT", secret)
    monkeypatch.setattr(portal, "WINDY_API_TOKEN_WEBCAMS", secret)
    body = client.get("/tokens").get_data(as_text=True)
    assert secret not in body
    assert "Configured" in body


def test_point_forecast_without_token_returns_none(monkeypatch):
    monkeypatch.setattr(portal, "WINDY_API_TOKEN_POINT", None)
    assert portal.fetch_real_windy_data() is None


def test_missing_tokens_reports_names_only(monkeypatch):
    monkeypatch.setitem(config.REQUIRED_TOKENS, "WINDY_API_TOKEN_MAP", None)
    assert "WINDY_API_TOKEN_MAP" in config.missing_tokens()

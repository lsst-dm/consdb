"""Tests for the write authorization dependency.

Gafaelfawr is replaced with a fake ``httpx.get``, and the database is never
touched: ``require_writer`` runs before the route's other dependencies, so
rejected requests never reach them.
"""

import time

import httpx
import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from lsst.consdb import dependencies, pqserver
from lsst.consdb.config import config
from lsst.consdb.dependencies import require_writer

GAFAELFAWR_URL = "https://gafaelfawr.example.com"
TOKEN_INFO_URL = f"{GAFAELFAWR_URL}/auth/api/v1/token-info"

TOKENS = {
    "gt-rapid-analysis": "bot-rapid-analysis",
    "gt-someone-else": "someuser",
}


class FakeGafaelfawr:
    """Stand-in for ``httpx.get`` that answers token-info requests."""

    def __init__(self) -> None:
        self.calls = 0
        self.error: Exception | None = None
        self.expires: int | None = None

    def __call__(self, url: str, *, headers: dict[str, str], timeout: float) -> httpx.Response:
        self.calls += 1
        if self.error:
            raise self.error
        assert url == TOKEN_INFO_URL
        request = httpx.Request("GET", url)
        token = headers["Authorization"].removeprefix("Bearer ")
        if token not in TOKENS:
            return httpx.Response(401, json={"detail": "Invalid token"}, request=request)
        info = {"username": TOKENS[token], "token_type": "service", "scopes": []}
        if self.expires is not None:
            info["expires"] = self.expires
        return httpx.Response(200, json=info, request=request)


@pytest.fixture
def gafaelfawr(monkeypatch):
    fake = FakeGafaelfawr()
    monkeypatch.setattr(dependencies.httpx, "get", fake)
    monkeypatch.setattr(config, "write_auth_enabled", True)
    monkeypatch.setattr(config, "allowed_writers", ["bot-rapid-analysis"])
    monkeypatch.setattr(config, "gafaelfawr_url", GAFAELFAWR_URL)
    dependencies.reset_dependencies()
    yield fake
    dependencies.reset_dependencies()


@pytest.fixture
def client():
    app = FastAPI()

    @app.post("/write")
    def write(username: str | None = Depends(require_writer)) -> dict[str, str | None]:
        return {"username": username}

    return TestClient(app)


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_disabled(client, monkeypatch):
    monkeypatch.setattr(config, "write_auth_enabled", False)
    r = client.post("/write")
    assert r.status_code == 200
    assert r.json() == {"username": None}


def test_allowed_writer(client, gafaelfawr):
    r = client.post("/write", headers=_auth("gt-rapid-analysis"))
    assert r.status_code == 200
    assert r.json() == {"username": "bot-rapid-analysis"}


def test_missing_token(client, gafaelfawr):
    r = client.post("/write")
    assert r.status_code == 401
    assert r.headers["WWW-Authenticate"] == "Bearer"
    assert gafaelfawr.calls == 0


def test_invalid_token(client, gafaelfawr):
    r = client.post("/write", headers=_auth("gt-bogus"))
    assert r.status_code == 401


def test_other_user_forbidden(client, gafaelfawr):
    r = client.post("/write", headers=_auth("gt-someone-else"))
    assert r.status_code == 403
    assert "someuser" in r.json()["detail"]


def test_gafaelfawr_unreachable(client, gafaelfawr):
    gafaelfawr.error = httpx.ConnectError("connection refused")
    r = client.post("/write", headers=_auth("gt-rapid-analysis"))
    assert r.status_code == 503


def test_cache(client, gafaelfawr):
    for _ in range(3):
        r = client.post("/write", headers=_auth("gt-rapid-analysis"))
        assert r.status_code == 200
    assert gafaelfawr.calls == 1


def test_cache_respects_token_expiry(client, gafaelfawr):
    gafaelfawr.expires = int(time.time()) - 1
    for _ in range(2):
        r = client.post("/write", headers=_auth("gt-rapid-analysis"))
        assert r.status_code == 200
    assert gafaelfawr.calls == 2


def test_real_route_rejects_before_touching_database(gafaelfawr):
    client = TestClient(pqserver.app)
    r = client.post(
        "/consdb/insert/lsstcam/visit1_quicklook/obs/1",
        json={"values": {}},
    )
    assert r.status_code == 401


def test_config_requires_gafaelfawr_url(monkeypatch):
    monkeypatch.setenv("WRITE_AUTH_ENABLED", "true")
    monkeypatch.delenv("GAFAELFAWR_URL", raising=False)
    with pytest.raises(ValueError, match="GAFAELFAWR_URL"):
        type(config)()

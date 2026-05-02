"""Cliente HTTP al servicio de estimación slicer (GET /machines, OAuth2 opcional)."""

from __future__ import annotations

import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def _fetch_oauth_access_token(base: str) -> str | None:
    client_id = (getattr(settings, "SLICER_OAUTH_CLIENT_ID", None) or "").strip()
    client_secret = (
        getattr(settings, "SLICER_OAUTH_CLIENT_SECRET", None) or ""
    ).strip()
    if not client_id or not client_secret:
        return None
    url = f"{base}/oauth/token"
    try:
        resp = requests.post(
            url,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )
    except requests.RequestException as exc:
        logger.warning("Slicer OAuth token request failed: %s", exc)
        return None
    if resp.status_code != 200:
        logger.warning(
            "Slicer OAuth token HTTP %s: %s", resp.status_code, resp.text[:200]
        )
        return None
    try:
        body = resp.json()
    except ValueError:
        return None
    token = body.get("access_token")
    return token if isinstance(token, str) else None


def fetch_slicer_machines() -> list[dict[str, str]]:
    """
    Devuelve [{'id': ..., 'name': ...}, ...] desde GET /machines.
    Con API_AUTH_ENABLED intenta client credentials si la primera petición devuelve 401.
    """
    base = (getattr(settings, "SLICER_HOST", None) or "").strip().rstrip("/")
    if not base:
        return []

    url = f"{base}/machines"

    def _get(headers: dict[str, str] | None) -> requests.Response | None:
        try:
            return requests.get(url, headers=headers or {}, timeout=15)
        except requests.RequestException as exc:
            logger.warning("Slicer GET /machines failed: %s", exc)
            return None

    resp = _get(None)
    if resp is None:
        return []
    if resp.status_code == 401:
        token = _fetch_oauth_access_token(base)
        if not token:
            return []
        resp = _get({"Authorization": f"Bearer {token}"})
        if resp is None:
            return []

    if resp.status_code != 200:
        logger.warning(
            "Slicer /machines HTTP %s: %s", resp.status_code, resp.text[:200]
        )
        return []

    try:
        data = resp.json()
    except ValueError:
        return []

    if not isinstance(data, list):
        return []

    out: list[dict[str, str]] = []
    for item in data:
        if isinstance(item, dict) and "id" in item and "name" in item:
            out.append({"id": str(item["id"]), "name": str(item["name"])})
    return out

from __future__ import annotations

import logging
from typing import BinaryIO

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def _slicer_base() -> str:
    return (getattr(settings, "SLICER_HOST", None) or "").strip().rstrip("/")


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


def _slicer_request(
    method: str,
    path: str,
    *,
    files: dict | None = None,
    data: dict | None = None,
    timeout: int = 15,
) -> requests.Response | None:
    """
    GET o POST a {SLICER_HOST}{path}. Si la API responde 401, reintenta con Bearer
    (client credentials) cuando hay credenciales OAuth configuradas.
    """
    base = _slicer_base()
    if not base:
        return None
    url = f"{base}{path}"
    method_u = method.upper()

    def _call(headers: dict[str, str]) -> requests.Response | None:
        try:
            if method_u == "GET":
                return requests.get(url, headers=headers, timeout=timeout)
            return requests.post(
                url, headers=headers, files=files, data=data, timeout=timeout
            )
        except requests.RequestException as exc:
            logger.warning("Slicer %s %s failed: %s", method_u, path, exc)
            return None

    resp = _call({})
    if resp is None:
        return None
    if resp.status_code == 401:
        token = _fetch_oauth_access_token(base)
        if not token:
            return resp
        if files:
            for spec in files.values():
                if isinstance(spec, tuple) and len(spec) >= 2:
                    inner = spec[1]
                    if hasattr(inner, "seek"):
                        try:
                            inner.seek(0)
                        except OSError:
                            pass
        resp = _call({"Authorization": f"Bearer {token}"})
    return resp


def _format_error_response(resp: requests.Response) -> str:
    try:
        body = resp.json()
    except ValueError:
        text = (resp.text or "").strip()
        return text[:800] if text else f"HTTP {resp.status_code}"
    detail = body.get("detail")
    if isinstance(detail, list):
        parts = []
        for item in detail:
            if isinstance(item, dict):
                loc = item.get("loc", ())
                msg = item.get("msg", "")
                parts.append(f"{'.'.join(str(x) for x in loc)}: {msg}")
            else:
                parts.append(str(item))
        return "; ".join(parts) if parts else f"HTTP {resp.status_code}"
    if detail is not None:
        return str(detail)
    return f"HTTP {resp.status_code}"


def fetch_slicer_machines() -> list[dict[str, str]]:
    """
    Devuelve [{'id': ..., 'name': ...}, ...] desde GET /machines.
    Con API_AUTH_ENABLED intenta client credentials si la primera petición devuelve 401.
    """
    resp = _slicer_request("GET", "/machines")
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


def post_slicer_estimate(
    *,
    file_obj: BinaryIO,
    filename: str,
    slicer_material: str,
    machine_id: str | None,
) -> tuple[dict[str, int | float] | None, str | None]:
    """
    POST /estimate (multipart). Devuelve ({"hours", "minutes", "grams"}, None) si OK,
    o (None, mensaje_error) si falla configuración, red, HTTP o JSON inválido.
    """
    base = _slicer_base()
    if not base:
        return None, "SLICER_HOST no está configurado."

    url_path = "/estimate"
    payload: dict[str, str] = {"material": slicer_material}
    if machine_id and str(machine_id).strip():
        payload["machine"] = str(machine_id).strip()

    files = {
        "source": (
            filename,
            file_obj,
            "application/octet-stream",
        )
    }

    resp = _slicer_request(
        "POST",
        url_path,
        files=files,
        data=payload,
        timeout=120,
    )
    if resp is None:
        return None, "No se pudo contactar al servicio slicer."

    if resp.status_code == 422:
        return None, _format_error_response(resp)

    if resp.status_code != 200:
        logger.warning(
            "Slicer /estimate HTTP %s: %s", resp.status_code, resp.text[:300]
        )
        return None, _format_error_response(resp)

    try:
        body = resp.json()
    except ValueError:
        return None, "La respuesta del slicer no es JSON válido."

    if not isinstance(body, dict):
        return None, "Respuesta del slicer con formato inesperado."

    try:
        hours = int(body["hours"])
        minutes = int(body["minutes"])
        grams = float(body["grams"])
    except (KeyError, TypeError, ValueError) as exc:
        return None, f"Respuesta del slicer incompleta: {exc}"

    if hours < 0 or not (0 <= minutes <= 59) or grams < 0:
        return None, "Respuesta del slicer con valores fuera de rango."

    return {"hours": hours, "minutes": minutes, "grams": grams}, None

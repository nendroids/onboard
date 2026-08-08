"""
Tests for public drive listings (approved jobs).
"""

import pytest
from flask.testing import FlaskClient


def test_list_approved_drives(client: FlaskClient, approved_job):
    resp = client.get("/api/v1/drives")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 1
    assert any(j["id"] == approved_job.id for j in data["items"])


def test_search_drives(client: FlaskClient, approved_job):
    resp = client.get("/api/v1/drives?q=Software")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["total"] >= 1
    assert data["items"][0]["title"] == "Software Engineer"


def test_get_single_drive(client: FlaskClient, approved_job):
    resp = client.get(f"/api/v1/drives/{approved_job.id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == approved_job.id
    assert data["title"] == "Software Engineer"
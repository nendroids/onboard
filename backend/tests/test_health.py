# def test_health_endpoint(client):
#     response = client.get("/api/v1/health")

#     assert response.status_code == 200
#     json_data = response.get_json()
#     assert json_data["status"] == "ok"
#     assert json_data["database"] == "ok"
#     assert json_data["cache"] == "ok"

"""
Health check endpoint tests.
"""

def test_health_check(client):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"
    assert data["cache"] == "ok"
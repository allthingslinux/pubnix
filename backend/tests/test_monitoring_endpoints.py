from fastapi.testclient import TestClient

import main


def test_prometheus_metrics_endpoint():
    client = TestClient(main.app)
    resp = client.get("/api/v1/monitoring/metrics")
    assert resp.status_code == 200
    assert b"pubnix_total_users" in resp.content


def test_health_alert():
    client = TestClient(main.app)
    resp = client.get("/api/v1/monitoring/alerts/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"

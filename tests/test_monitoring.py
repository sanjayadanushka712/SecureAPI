from fastapi.testclient import TestClient

from app.main import app
from app.monitoring import CONTENT_TYPE


def _request_total(client: TestClient) -> float:
    response = client.get("/metrics")
    line = next(
        line
        for line in response.text.splitlines()
        if line.startswith("http_requests_total ")
    )
    return float(line.split(" ", 1)[1])


def test_metrics_endpoint_returns_prometheus_text():
    with TestClient(app) as client:
        response = client.get("/metrics")

    assert response.status_code == 200
    assert response.headers["content-type"] == CONTENT_TYPE
    assert "http_requests_total" in response.text


def test_health_request_increments_request_counter():
    with TestClient(app) as client:
        before = _request_total(client)
        response = client.get("/health")
        after = _request_total(client)

    assert response.status_code == 200
    assert after > before

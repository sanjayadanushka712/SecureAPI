import socket
import threading
import time

import httpx
import pytest
import uvicorn

from app.main import app


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="module")
def live_server_url():
    port = _free_port()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    deadline = time.time() + 10
    while not server.started:
        if time.time() > deadline:
            raise RuntimeError("uvicorn did not start in time")
        time.sleep(0.05)

    yield f"http://127.0.0.1:{port}"

    server.should_exit = True
    thread.join(timeout=10)


def test_real_server_health_check(live_server_url):
    response = httpx.get(f"{live_server_url}/health", timeout=5)

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_real_server_rejects_unknown_route(live_server_url):
    response = httpx.get(f"{live_server_url}/does-not-exist", timeout=5)

    assert response.status_code == 404

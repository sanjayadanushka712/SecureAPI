import re
import threading

CONTENT_TYPE = "text/plain; version=0.0.4; charset=utf-8"

_MAX_SERIES = 1000
_UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)

_lock = threading.Lock()
_requests_total = 0
_errors_total = 0
_requests_by_route: dict[tuple[str, str, str], int] = {}
_errors_by_route: dict[tuple[str, str, str], int] = {}
_latency_sum = 0.0
_latency_count = 0
_latency_by_route: dict[tuple[str, str, str], tuple[float, int]] = {}
_in_flight = 0


def _escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


def _safe_path(path: str) -> str:
    segments = []
    for segment in str(path).split("/"):
        if segment.isdigit():
            segments.append("{id}")
        elif _UUID_PATTERN.fullmatch(segment):
            segments.append("{uuid}")
        else:
            segments.append(segment)
    return "/".join(segments) or "/"


def _labels(method: str, path: str, status: int | str) -> tuple[str, str, str]:
    labels = (str(method), _safe_path(path), str(status))
    if labels not in _requests_by_route and len(_requests_by_route) >= _MAX_SERIES:
        return (labels[0], "other", labels[2])
    return labels


def _is_error(status: int | str) -> bool:
    try:
        return int(status) >= 500
    except (TypeError, ValueError):
        return False


def observe(method: str, path: str, status: int | str, duration: float) -> None:
    global _requests_total, _errors_total, _latency_sum, _latency_count

    with _lock:
        labels = _labels(method, path, status)
        _requests_total += 1
        _requests_by_route[labels] = _requests_by_route.get(labels, 0) + 1

        if _is_error(status):
            _errors_total += 1
            _errors_by_route[labels] = _errors_by_route.get(labels, 0) + 1

        seconds = max(0.0, float(duration))
        _latency_sum += seconds
        _latency_count += 1
        total, count = _latency_by_route.get(labels, (0.0, 0))
        _latency_by_route[labels] = (total + seconds, count + 1)


def inc_in_flight() -> None:
    global _in_flight

    with _lock:
        _in_flight += 1


def dec_in_flight() -> None:
    global _in_flight

    with _lock:
        _in_flight = max(0, _in_flight - 1)


def reset() -> None:
    global _requests_total, _errors_total, _latency_sum, _latency_count, _in_flight

    with _lock:
        _requests_total = 0
        _errors_total = 0
        _requests_by_route.clear()
        _errors_by_route.clear()
        _latency_sum = 0.0
        _latency_count = 0
        _latency_by_route.clear()
        _in_flight = 0


def _sample(name: str, labels: tuple[str, str, str], value: object) -> str:
    method, path, status = (_escape(part) for part in labels)
    return f'{name}{{method="{method}",path="{path}",status="{status}"}} {value}'


def render() -> str:
    with _lock:
        lines = [
            "# HELP http_requests_total Total HTTP requests observed.",
            "# TYPE http_requests_total counter",
            f"http_requests_total {_requests_total}",
            "# HELP http_requests_by_route_total HTTP requests by method, route "
            "and status.",
            "# TYPE http_requests_by_route_total counter",
        ]
        lines.extend(
            _sample("http_requests_by_route_total", labels, value)
            for labels, value in sorted(_requests_by_route.items())
        )
        lines.extend(
            [
                "# HELP http_errors_total Total HTTP requests with a 5xx status.",
                "# TYPE http_errors_total counter",
                f"http_errors_total {_errors_total}",
                "# HELP http_errors_by_route_total HTTP 5xx responses by method, "
                "route and status.",
                "# TYPE http_errors_by_route_total counter",
            ]
        )
        lines.extend(
            _sample("http_errors_by_route_total", labels, value)
            for labels, value in sorted(_errors_by_route.items())
        )
        lines.extend(
            [
                "# HELP http_request_duration_seconds HTTP request latency in seconds.",
                "# TYPE http_request_duration_seconds summary",
                f"http_request_duration_seconds_sum {_latency_sum:.6f}",
                f"http_request_duration_seconds_count {_latency_count}",
                "# HELP http_request_duration_by_route_seconds Latency by method, "
                "route and status.",
                "# TYPE http_request_duration_by_route_seconds summary",
            ]
        )
        for labels, (total, count) in sorted(_latency_by_route.items()):
            lines.append(
                _sample(
                    "http_request_duration_by_route_seconds_sum", labels, f"{total:.6f}"
                )
            )
            lines.append(
                _sample("http_request_duration_by_route_seconds_count", labels, count)
            )
        lines.extend(
            [
                "# HELP http_requests_in_flight HTTP requests currently being "
                "processed.",
                "# TYPE http_requests_in_flight gauge",
                f"http_requests_in_flight {_in_flight}",
            ]
        )

    return "\n".join(lines) + "\n"

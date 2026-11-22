from collections.abc import Iterator
from contextlib import contextmanager

from opentelemetry import trace
from opentelemetry.trace import Span

tracer = trace.get_tracer("secureapi", "1.0.0")


@contextmanager
def span(name: str, **attributes: object) -> Iterator[Span]:
    with tracer.start_as_current_span(name, attributes=attributes) as active_span:
        yield active_span


@contextmanager
def task_span(operation: str, **attributes: object) -> Iterator[Span]:
    with span(f"task.{operation}", **attributes) as active_span:
        yield active_span

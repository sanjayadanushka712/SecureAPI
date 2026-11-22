import time

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

from app.monitoring import (
    CONTENT_TYPE,
    dec_in_flight,
    inc_in_flight,
    observe,
    render,
)
from app.routes.profile import router as profile_router
from app.routes.tasks import router as tasks_router
from app.telemetry import span, task_span

app = FastAPI(
    title="SecureAPI",
    description="A secure backend API platform",
    version="1.0.0",
)

app.include_router(tasks_router)
app.include_router(profile_router)


@app.middleware("http")
async def observe_requests(request: Request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)

    method = request.method
    target = request.url.path
    status = 500
    started = time.perf_counter()
    inc_in_flight()
    try:
        with span("http.request", http_method=method, http_target=target):
            if method == "POST" and target.startswith("/tasks"):
                with task_span("create", http_method=method, http_route=target):
                    response = await call_next(request)
            else:
                response = await call_next(request)
        status = response.status_code
        return response
    finally:
        dec_in_flight()
        route = request.scope.get("route")
        route_path = getattr(route, "path", None) or target
        observe(method, route_path, status, time.perf_counter() - started)


@app.get("/metrics", include_in_schema=False)
def metrics():
    return PlainTextResponse(render(), media_type=CONTENT_TYPE)


@app.get("/")
def root():
    return {"message": "Welcome to SecureAPI"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

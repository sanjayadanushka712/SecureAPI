from fastapi import FastAPI, Depends, HTTPException, status

from app.routes.tasks import router as tasks_router
from app.routes.profile import router as profile_router

app = FastAPI(
    title="SecureAPI",
    description="A secure backend API platform",
    version="1.0.0",
)

app.include_router(tasks_router)
app.include_router(profile_router)


@app.get("/")
def root():
    return {"message": "Welcome to SecureAPI"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(tags=["Profile"])


def get_current_user():
    return {"id": 1, "username": "admin"}


def get_active_user(user: dict = Depends(get_current_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    return user


@router.get("/profile")
def get_profile(user: dict = Depends(get_active_user)):
    return {
        "message": "User profile",
        "user": user,
    }

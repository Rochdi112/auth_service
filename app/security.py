from fastapi import Depends, HTTPException, status
from .auth import get_current_user
from .models import User

def require_role(required_role: str):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès réservé au rôle '{required_role}'"
            )
        return user
    return Depends(wrapper)

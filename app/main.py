# app/main.py

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from contextlib import asynccontextmanager

from sqlmodel import Session, select
from app.models import User
from app.routes import router
from app.database import create_db_and_tables
from app.security import require_role
from app.database import get_db as get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Auth Service",
    version="1.0",
    lifespan=lifespan
)

# Inclusion des routes
app.include_router(router)

@app.delete("/users/{user_id}", dependencies=[require_role("admin")])
async def delete_user(
    user_id: int,
    session: Annotated[Session, Depends(get_session)]
):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    session.delete(user)
    session.commit()
    return {"detail": f"Utilisateur {user.email} supprimé"}

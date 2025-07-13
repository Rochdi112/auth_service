from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from .models import User
from .schemas import UserCreate, UserRead, Token, UserUpdate
from .auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from .security import require_role
from .logger import logger
from typing import Annotated
from app.database import get_db as get_session




router = APIRouter()


@router.post("/register", response_model=UserRead)
def register(user_create: UserCreate, db: Session = Depends(get_session)):
    # Vérifier si l'email existe déjà
    existing_user = db.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    # Hachage + création utilisateur
    hashed_password = get_password_hash(user_create.password)
    user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        role=user_create.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f"Nouvel utilisateur enregistré : {user.email} ({user.role})")
    return user


@router.post("/login", response_model=Token)
def login(user_create: UserCreate, db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.email == user_create.email)).first()
    if not user or not verify_password(user_create.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Utilisateur désactivé")

    access_token = create_access_token(data={"sub": user.email})
    logger.info(f"Connexion réussie pour {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user", response_model=UserRead)
def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/roles")
def get_roles(current_user: User = require_role("admin")):
    return ["admin", "technicien", "client"]

# PATCH - Mise à jour partielle d’un utilisateur (admin uniquement)
@router.patch("/users/{user_id}", dependencies=[require_role("admin")])
def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Annotated[Session, Depends(get_session)]
):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/users", response_model=list[UserRead], dependencies=[require_role("admin")])
def list_users(session: Annotated[Session, Depends(get_session)]):
    return session.exec(select(User)).all()

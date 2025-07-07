from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from .models import User
from .schemas import UserCreate, UserRead, Token
from .auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from .database import get_db
from .security import require_role
from .logger import logger

router = APIRouter()


@router.post("/register", response_model=UserRead)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
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
def login(user_create: UserCreate, db: Session = Depends(get_db)):
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

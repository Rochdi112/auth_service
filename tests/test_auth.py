import pytest
import os
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, select
from app.main import app
import python_multipart

from app.database import engine
from app.models import User

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def reset_database():
    # Supprime la base de données SQLite pour recréer avec tous les champs
    if os.path.exists("auth.db"):
        os.remove("auth.db")
    SQLModel.metadata.create_all(engine)

def test_register_and_login():
    email = "admin3@example.com"
    password = "secret123"
    role = "admin"

    # Enregistrement
    response = client.post("/register", json={
        "email": email,
        "password": password,
        "role": role
    })
    assert response.status_code == 200
    assert response.json()["email"] == email

    # Connexion
    response = client.post("/login", json={
        "email": email,
        "password": password,
        "role": role
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token

    # Accès /user
    response = client.get("/user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == email

    # Accès /me
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == email

    # Accès /roles
    response = client.get("/roles", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "admin" in response.json()

def test_protected_without_token():
    response = client.get("/user")
    assert response.status_code == 401

def test_register_email_duplicate():
    response = client.post("/register", json={
        "email": "admin3@example.com",
        "password": "anotherpass",
        "role": "admin"
    })
    assert response.status_code == 400
    assert "déjà utilisé" in response.text.lower()

def test_login_wrong_password():
    response = client.post("/login", json={
        "email": "admin4@example.com",
        "password": "wrongpassword",
        "role": "admin"
    })
    assert response.status_code == 401

def test_roles_access_denied_for_non_admin():
    email = "tech@example.com"
    password = "techpass"

    client.post("/register", json={
        "email": email,
        "password": password,
        "role": "technicien"
    })

    response = client.post("/login", json={
        "email": email,
        "password": password,
        "role": "technicien"
    })
    token = response.json()["access_token"]

    response = client.get("/roles", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_login_user_inactive():
    email = "inactive@example.com"
    password = "test123"
    role = "admin"

    response = client.post("/register", json={
        "email": email,
        "password": password,
        "role": role
    })
    assert response.status_code == 200

    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        user.is_active = False
        session.add(user)
        session.commit()

    response = client.post("/login", json={
        "email": email,
        "password": password,
        "role": role
    })
    assert response.status_code == 403
    assert "désactivé" in response.text.lower()

def test_patch_update_user():

    # 1. Créer un utilisateur admin
    response = client.post("/register", json={
        "email": "admin_update@example.com",
        "password": "test123",
        "role": "admin"
    })
    assert response.status_code == 200
    admin_data = response.json()
    user_id = admin_data["id"]

    # 2. Connexion pour obtenir le token JWT
    login_response = client.post("/login", json={
        "email": "admin_update@example.com",
        "password": "test123",
        "role": "admin"  # ✅ Ajout obligatoire
})

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Mise à jour partielle (modifie le rôle et is_active)
    patch_response = client.patch(f"/users/{user_id}", json={
        "role": "technicien",
        "is_active": False
    }, headers=headers)

    assert patch_response.status_code == 200
    updated_user = patch_response.json()
    assert updated_user["role"] == "technicien"
    assert updated_user["is_active"] == False
    assert updated_user["email"] == "admin_update@example.com"


def test_delete_user():
    # 1. Création d’un utilisateur admin
    response = client.post("/register", json={
        "email": "delete_me@example.com",
        "password": "delete123",
        "role": "admin"
    })
    assert response.status_code == 200
    user_id = response.json()["id"]

    # 2. Connexion admin pour obtenir le token JWT
    login = client.post("/login", json={
        "email": "delete_me@example.com",
        "password": "delete123",
        "role": "admin"  # obligatoire dans ton schéma actuel
    })
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Suppression de l’utilisateur
    delete_response = client.delete(f"/users/{user_id}", headers=headers)
    assert delete_response.status_code == 200
    assert "supprimé" in delete_response.json()["detail"].lower()

    # 4. Vérifie que l’utilisateur est bien inaccessible (token invalidé)
    #    Cela provoque une erreur 401 car le user n'existe plus en base
    get_response = client.patch(f"/users/{user_id}", json={"role": "client"}, headers=headers)
    assert get_response.status_code == 401  # 401 Unauthorized attendu
    # Création d’un utilisateur admin
    response = client.post("/register", json={
        "email": "delete_me@example.com",
        "password": "delete123",
        "role": "admin"
    })
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Connexion admin pour obtenir le token
    login = client.post("/login", json={
        "email": "delete_me@example.com",
        "password": "delete123",
        "role": "admin"  # 🔥 obligatoire pour respecter le schéma UserCreate
})

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Suppression
    delete_response = client.delete(f"/users/{user_id}", headers=headers)
    assert delete_response.status_code == 200
    assert "supprimé" in delete_response.json()["detail"].lower()

    # Vérifie que l’utilisateur n’existe plus
    get_response = client.patch(f"/users/{user_id}", json={"role": "client"}, headers=headers)
    assert get_response.status_code == 401  # Le token est refusé car l'utilisateur a été supprimé
    
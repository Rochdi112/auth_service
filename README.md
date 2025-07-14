# 🔐 Auth Service – Mini ERP MIF Maroc

Ce microservice assure l’authentification, la gestion des utilisateurs et des rôles dans le projet Mini ERP MIF Maroc. Il est conçu avec FastAPI et SQLModel, et il est sécurisé via JWT.

---

## 🚀 Fonctionnalités

| Route                          | Méthode | Description                                          | Accès        |
|-------------------------------|---------|------------------------------------------------------|--------------|
| `/register`                   | POST    | Créer un utilisateur (email, mot de passe, rôle)     | Public       |
| `/login`                      | POST    | Authentifie un utilisateur, retourne un JWT          | Public       |
| `/user`                       | GET     | Renvoie l’utilisateur connecté                       | Authentifié  |
| `/me`                         | GET     | Alias de `/user`, pour compatibilité                 | Authentifié  |
| `/roles`                      | GET     | Retourne les rôles disponibles                       | Admin        |
| `/users`                      | GET     | Liste tous les utilisateurs                          | Admin        |
| `/users/{user_id}`            | PATCH   | Mise à jour partielle (email, rôle, statut)          | Admin        |
| `/users/{user_id}`            | DELETE  | Supprime un utilisateur                              | Admin        |

---

## 🧰 Stack technique

- `FastAPI`
- `SQLModel` + SQLite (dev) / PostgreSQL (prod)
- `passlib[bcrypt]` – Hachage mot de passe
- `python-jose` – JWT
- `pytest` – Tests unitaires
- `httpx.TestClient` – Client de test

---

## 🔐 Sécurité

- Authentification via JWT
- Vérification automatique du rôle (`admin`, `technicien`, `client`)
- Récupération de l’utilisateur connecté via dépendance `get_current_user()`

---

## ✅ Tests unitaires

Lancement des tests :

```bash
pytest -v
```

Tous les tests critiques sont couverts :
- Enregistrement
- Connexion (valide et erreurs)
- Récupération des infos protégées
- Modification d’utilisateur (`PATCH`)
- Suppression (`DELETE`)
- Contrôle des rôles

---

## 🏗️ Structure du projet

```
auth_service/
├── app/
│   ├── main.py          # Création app + routes
│   ├── models.py        # SQLModel User
│   ├── schemas.py       # Schémas Pydantic v2
│   ├── routes.py        # Routes protégées
│   ├── auth.py          # JWT, sécurité
│   ├── security.py      # Rôles requis
│   ├── database.py      # Connexion DB
│   ├── logger.py        # Logging
│   └── tests/
│       └── test_auth.py # Tests unitaires
```

---

## 🐳 Dockerisation (exemple)

```Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📬 Contact

Projet développé pour MIF Maroc – Service Informatique – 2025
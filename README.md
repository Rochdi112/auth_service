Voici le contenu final propre et professionnel de ton `README.md` prêt à être copié dans ton projet `auth_service/README.md` :

---

````markdown
# 🛡️ Auth Service — Microservice d’Authentification
**Mini ERP — MIF Maroc**  
**Auteur : Rochdi | Génie Informatique**  
**Encadrant : Mr Lahlou**

---

## 🎯 Objectif du Microservice

Le microservice `auth_service` assure les fonctionnalités critiques suivantes :

- Gestion des utilisateurs (inscription, connexion)
- Authentification par token JWT
- Attribution et vérification des rôles (`admin`, `technicien`, `medecin`)
- Sécurisation des routes par dépendance et autorisation
- Rejet des utilisateurs désactivés

Ce service est totalement découplé, prêt à être intégré dans une architecture microservices avec d'autres modules métiers (clients, techniciens, interventions, etc.).

---

## ⚙️ Architecture Technique

| Élément           | Technologie utilisée         |
|-------------------|------------------------------|
| Langage           | Python 3.11                  |
| Framework API     | FastAPI                      |
| ORM               | SQLModel (SQLite)            |
| Authentification  | JWT via `python-jose`        |
| Sécurité          | Hashage avec Passlib (`bcrypt`) |
| Tests             | Pytest, httpx                |
| Conteneurisation  | Docker, Docker Compose       |

---

## 📚 Endpoints RESTful

| Méthode | Endpoint     | Rôle requis | Description                          |
|--------:|--------------|-------------|--------------------------------------|
| POST    | `/register`  | Public      | Crée un utilisateur                  |
| POST    | `/login`     | Public      | Authentifie et retourne un JWT       |
| GET     | `/user`      | JWT         | Récupère l’utilisateur connecté      |
| GET     | `/me`        | JWT         | Alias de `/user`                     |
| GET     | `/roles`     | `admin`     | Liste des rôles disponibles          |

---

## 🔐 Sécurité et Bonnes Pratiques

- Authentification basée sur JWT signés avec clé secrète
- Hashage sécurisé des mots de passe (`bcrypt`)
- Système de rôles intégré au cœur de la logique applicative
- Sécurisation des routes critiques via :
  ```python
  Depends(get_current_user)
````

* Vérification explicite des droits :

  ```python
  if current_user.role != "admin":
      raise HTTPException(status_code=403, detail="Not authorized")
  ```

---

## 🧪 Tests Unitaires

L’ensemble des tests couvre les cas suivants :

* ✅ Inscription et connexion (`test_register_and_login`)
* 🔒 Rejet sans token (`test_protected_without_token`)
* 📧 Email déjà enregistré (`test_register_email_duplicate`)
* ❌ Mauvais mot de passe (`test_login_wrong_password`)
* ⛔ Accès interdit aux rôles non-admin (`test_roles_access_denied_for_non_admin`)
* 🚫 Rejet utilisateur inactif (`test_login_user_inactive`)

Commandes de test :

```bash
pytest -v
```

---

## 🐳 Déploiement Docker

### 🛠 Build manuel

```bash
docker build -t auth_service .
docker run -p 8000:8000 auth_service
```

### ⚙️ Via Docker Compose

```yaml
version: "3.8"

services:
  auth_service:
    build: .
    ports:
      - "8000:8000"
    restart: always
```

---

## 📂 Structure du Projet

AUTH_SERVICE/
├── .pytest_cache/               # Cache des tests Pytest
├── .venv/                       # Environnement virtuel Python (non versionné)
│
├── app/                         # Code principal de l'application FastAPI
│   ├── __init__.py
│   ├── auth.py                  # Fonctions JWT, vérification, création de tokens
│   ├── config.py                # Configuration (JWT_SECRET, durée, algo, etc.)
│   ├── database.py              # Connexion à la base de données (SQLModel/SQLite)
│   ├── logger.py                # Logger configurable (optionnel, propreté logs)
│   ├── main.py                  # Entrée FastAPI (inclut les routes et init DB)
│   ├── models.py                # Modèle User (SQLModel) avec is_active, role, etc.
│   ├── routes.py                # Déclaration des endpoints `/register`, `/login`, etc.
│   ├── schemas.py               # Schémas Pydantic pour validation des requêtes
│   └── security.py              # Hashage, vérif mot de passe (Passlib)
│
├── tests/                       # Tests unitaires
│   ├── __init__.py
│   └── test_auth.py             # Tous les tests couverts (✅ 6/6)
│
├── .env                         # Variables d’environnement (non versionné)
├── .env.example                 # Exemple du fichier `.env` à copier
├── Dockerfile                   # Image Docker du microservice
├── docker-compose.yml           # Lancement via Docker Compose
├── requirements.txt             # Dépendances Python
└── README.md                    # Documentation technique (génie informatique)


## ✅ Statut

✔️ Fonctionnel
✔️ 100% des tests unitaires passent
⚠️ Aucune vulnérabilité connue détectée

---

## 🔄 Prochaine Étape

➡️ Intégration avec les microservices suivants :

* `clients_service`
* `techniciens_service`
* `interventions_service`

---

> Ce microservice est une brique essentielle de l’architecture distribuée du Mini ERP de gestion des interventions pour **MIF Maroc**.

```
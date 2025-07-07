# 🐍 Image de base
FROM python:3.11-slim

# 📁 Répertoire de travail
WORKDIR /app

# 📦 Copie des fichiers
COPY . /app

# 🔧 Installation des dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 🚀 Lancement de l'application FastAPI avec Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

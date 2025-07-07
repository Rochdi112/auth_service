import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis un fichier .env local

# Clé secrète pour JWT
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# URL de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")

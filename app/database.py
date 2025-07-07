from sqlmodel import create_engine, Session
from .config import DATABASE_URL

# Connexion à la base de données
engine = create_engine(DATABASE_URL, echo=False)

# Fonction de session pour les routes
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# Session directe pour usage interne (ex: get_current_user)
SessionLocal = Session(engine)

from fastapi import FastAPI
from app.routes import router
from app.database import create_db_and_tables

app = FastAPI(title="Auth Service", version="1.0")

# Initialisation de la base de données
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Inclusion des routes
app.include_router(router)

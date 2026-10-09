import os
from fastapi import FastAPI, HTTPException
import psycopg2

app = FastAPI(title="DevOps Junior Demo API")

# Citim configurația din Variabile de Mediu (cele mai bune practici Cloud)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")


def check_db_connection():
    """Verifică dacă baza de date este accesibilă."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            connect_timeout=3
        )
        conn.close()
        return True
    except Exception:
        return False


@app.get("/")
def read_root():
    """Ruta principală."""
    return {"message": "Hello, Cloud & DevOps World!", "status": "running"}


@app.get("/health")
def health_check():
    """Endpoint de Healthcheck folosit de Kubernetes / Load Balancers."""
    db_ok = check_db_connection()

    if not db_ok:
        # Returnează HTTP 500 dacă baza de date nu răspunde
        raise HTTPException(
            status_code=500,
            detail={"status": "unhealthy", "database": "disconnected"}
        )

    return {"status": "healthy", "database": "connected"}
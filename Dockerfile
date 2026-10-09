# Stage 1: Build & Dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Instalăm dependențele într-un director virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Runtime Image (Imagine extrem de mică și sigură)
FROM python:3.11-slim

WORKDIR /app

# Copiem doar mediul virtual din etapa de build
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiem codul aplicației
COPY main.py .

# Utilizator non-root pentru securitate
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Comanda de start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
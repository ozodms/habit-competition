#!/usr/bin/env bash
set -e

echo "Waiting for PostgreSQL..."
python - <<'PY'
import os, time, psycopg
host=os.getenv("POSTGRES_HOST","db")
port=os.getenv("POSTGRES_PORT","5432")
user=os.getenv("POSTGRES_USER","habituser")
pwd =os.getenv("POSTGRES_PASSWORD","habitpass")
db  =os.getenv("POSTGRES_DB","habitdb")
dsn=f"host={host} port={port} user={user} password={pwd} dbname={db}"
for _ in range(30):
    try:
        with psycopg.connect(dsn, connect_timeout=2) as conn:
            break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("Database not available")
PY

python manage.py migrate --noinput
exec python manage.py runserver 0.0.0.0:8000

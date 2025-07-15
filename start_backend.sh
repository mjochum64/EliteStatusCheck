#!/bin/bash
# Startskript für EliteStatusCheck Backend
# Stellt sicher, dass .env geladen wird, die conda-Umgebung aktiv ist und der Server im LAN erreichbar ist

# Verzeichnis des Skripts ermitteln
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# conda Umgebung aktivieren
if command -v conda &> /dev/null; then
  eval "$(conda shell.bash hook)"
  conda activate elite
else
  echo "[WARN] conda nicht gefunden. Bitte manuell aktivieren, falls benötigt."
fi

# .env laden (falls vorhanden)
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Backend starten (LAN erreichbar)
uvicorn elite_status.main:app --host 0.0.0.0 --port 8000

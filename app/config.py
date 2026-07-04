"""Configuração centralizada — carrega variáveis de ambiente."""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── LLM ──────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ── Gmail SMTP ───────────────────────────────────────
GMAIL_USER: str = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD", "")

# ── Google Sheets ────────────────────────────────────
SPREADSHEET_NAME: str = os.getenv("SPREADSHEET_NAME", "Informações - Dragon Ball Super")

def get_google_credentials() -> dict:
    """Retorna as credenciais do Google Service Account.
    
    Prioridade:
      1. Variável de ambiente GOOGLE_CREDENTIALS (JSON string) — ideal para deploy.
      2. Arquivo referenciado por GOOGLE_CREDENTIALS_FILE — ideal para dev local.
    """
    raw = os.getenv("GOOGLE_CREDENTIALS")
    if raw:
        return json.loads(raw)

    cred_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "")
    if cred_file:
        # Caminho absoluto ou relativo à raiz do projeto
        path = Path(cred_file)
        if not path.is_absolute():
            path = Path(__file__).resolve().parent.parent / cred_file
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))

    raise RuntimeError(
        "Google credentials não encontradas. "
        "Configure GOOGLE_CREDENTIALS (JSON string) ou GOOGLE_CREDENTIALS_FILE (caminho do .json)."
    )

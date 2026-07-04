"""Tools do agente — implementações das funções que o LLM pode chamar."""

import json
import logging
import smtplib
import traceback
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import httpx
import gspread
from google.oauth2.service_account import Credentials

from app.config import (
    GMAIL_USER,
    GMAIL_APP_PASSWORD,
    SPREADSHEET_NAME,
    get_google_credentials,
)

logger = logging.getLogger(__name__)

# ── Definições das tools para OpenAI Function Calling ──────────────

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "buscar_personagem",
            "description": "Busca informações de um personagem de Dragon Ball Super pelo ID numérico (1-44).",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "ID do personagem (1 a 44)",
                    }
                },
                "required": ["id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "salvar_planilha",
            "description": "Salva os dados do personagem na planilha Google Sheets 'Informações - Dragon Ball Super'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "description": "ID do personagem"},
                    "name": {"type": "string", "description": "Nome do personagem"},
                    "ki": {"type": "string", "description": "Poder Ki base"},
                    "maxKi": {"type": "string", "description": "Poder Ki máximo"},
                    "race": {"type": "string", "description": "Raça do personagem"},
                    "gender": {"type": "string", "description": "Gênero"},
                    "affiliation": {"type": "string", "description": "Afiliação"},
                    "image": {"type": "string", "description": "URL da imagem"},
                },
                "required": ["id", "name", "ki", "maxKi", "race", "gender", "affiliation", "image"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "enviar_email",
            "description": "Envia as informações do personagem por e-mail para o destinatário informado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "destinatario": {
                        "type": "string",
                        "description": "Endereço de e-mail do destinatário",
                    },
                    "conteudo": {
                        "type": "string",
                        "description": "Texto completo com as informações do personagem",
                    },
                    "nome_personagem": {
                        "type": "string",
                        "description": "Nome do personagem (usado no assunto do e-mail)",
                    },
                },
                "required": ["destinatario", "conteudo", "nome_personagem"],
            },
        },
    },
]


# ── Implementações ─────────────────────────────────────────────────

async def buscar_personagem(id: int) -> str:
    """Faz GET na Dragon Ball API e retorna os dados em JSON string."""
    url = f"https://dragonball-api.com/api/characters/{id}"
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url)

    if resp.status_code != 200:
        return json.dumps({"error": f"Personagem com ID {id} não encontrado."})

    data = resp.json()
    # Extrair somente os campos relevantes
    result = {
        "id": data.get("id"),
        "name": data.get("name"),
        "ki": data.get("ki"),
        "maxKi": data.get("maxKi"),
        "race": data.get("race"),
        "gender": data.get("gender"),
        "affiliation": data.get("affiliation"),
        "image": data.get("image"),
    }
    return json.dumps(result, ensure_ascii=False)


def salvar_planilha(
    id: int,
    name: str,
    ki: str,
    maxKi: str,
    race: str,
    gender: str,
    affiliation: str,
    image: str,
) -> str:
    """Adiciona uma linha na planilha do Google Sheets."""
    try:
        logger.info(f"[SHEETS] Tentando salvar na planilha: '{SPREADSHEET_NAME}'")
        creds_info = get_google_credentials()
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        credentials = Credentials.from_service_account_info(creds_info, scopes=scopes)
        gc = gspread.authorize(credentials)

        spreadsheet = gc.open(SPREADSHEET_NAME)
        worksheet = spreadsheet.sheet1

        row = [str(id), name, ki, maxKi, race, gender, affiliation, image]
        worksheet.append_row(row, value_input_option="USER_ENTERED")

        logger.info(f"[SHEETS] ✅ Dados de '{name}' salvos com sucesso.")
        return json.dumps({"status": "success", "message": "Dados salvos na planilha com sucesso."})
    except gspread.exceptions.SpreadsheetNotFound:
        err = f"Planilha '{SPREADSHEET_NAME}' não encontrada. Verifique se o nome está correto e se a Service Account tem acesso."
        logger.error(f"[SHEETS] ❌ {err}")
        return json.dumps({"status": "error", "message": err})
    except Exception as e:
        logger.error(f"[SHEETS] ❌ Erro: {str(e)}\n{traceback.format_exc()}")
        return json.dumps({"status": "error", "message": f"Erro ao salvar na planilha: {str(e)}"})


def enviar_email(destinatario: str, conteudo: str, nome_personagem: str) -> str:
    """Envia e-mail via Gmail SMTP com as informações do personagem."""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🐉 Dragon Ball Super — Informações de {nome_personagem}"
        msg["From"] = GMAIL_USER
        msg["To"] = destinatario

        # Corpo em texto simples
        text_part = MIMEText(conteudo, "plain", "utf-8")

        # Simple markdown to HTML parsing for the email
        html_body = conteudo
        # Images: ![alt](url) -> <img src="url" alt="alt" style="...">
        html_body = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<br><img src="\2" alt="\1" style="max-width:100%; max-height:300px; border-radius:12px; margin-top:10px;"><br>', html_body)
        # Bold: **text** -> <strong>text</strong>
        html_body = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html_body)

        # Corpo em HTML para melhor formatação
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px; background: #1a1a2e; color: #eee;">
            <div style="max-width: 600px; margin: 0 auto; background: #16213e; border-radius: 12px; padding: 24px; border: 1px solid #0f3460;">
                <h2 style="color: #e94560; margin-top: 0;">🐉 {nome_personagem}</h2>
                <div style="white-space: pre-wrap; line-height: 1.7;">{html_body}</div>
                <hr style="border-color: #0f3460; margin: 20px 0;">
                <p style="font-size: 12px; color: #888;">
                    Enviado automaticamente pelo <strong>Ajudante do desenvolvedor Nathanael Jorge</strong> — 
                    Agente de IA especialista em Dragon Ball Super.
                </p>
            </div>
        </body>
        </html>
        """
        html_part = MIMEText(html_content, "html", "utf-8")

        msg.attach(text_part)
        msg.attach(html_part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, destinatario, msg.as_string())

        return json.dumps({"status": "success", "message": "E-mail enviado com sucesso."})
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Erro ao enviar e-mail: {str(e)}"})


# ── Dispatcher — mapeia nome da tool → função ──────────────────────

TOOL_FUNCTIONS = {
    "buscar_personagem": buscar_personagem,
    "salvar_planilha": salvar_planilha,
    "enviar_email": enviar_email,
}


async def execute_tool(name: str, arguments: dict) -> str:
    """Executa a tool correspondente e retorna o resultado como string."""
    func = TOOL_FUNCTIONS.get(name)
    if not func:
        return json.dumps({"error": f"Tool '{name}' não encontrada."})

    # buscar_personagem é async, as demais são sync
    if name == "buscar_personagem":
        return await func(**arguments)
    else:
        return func(**arguments)

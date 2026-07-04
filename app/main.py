"""FastAPI — ponto de entrada da aplicação."""

import logging
logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel

from app.agent import chat

# ── App ────────────────────────────────────────────────
app = FastAPI(
    title="Ajudante do desenvolvedor Nathanael Jorge",
    description="Agente de IA especialista em Dragon Ball Super",
    version="1.0.0",
)

# ── Static Files ───────────────────────────────────────
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── Models ─────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatResponse(BaseModel):
    response: str
    status: str = "success"


# ── Routes ─────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve a página principal do chat."""
    index_path = STATIC_DIR / "index.html"
    return HTMLResponse(content=index_path.read_text(encoding="utf-8"))


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    """Recebe mensagem do usuário e retorna resposta do agente."""
    try:
        response_text = await chat(req.session_id, req.message)
        return ChatResponse(response=response_text, status="success")
    except Exception as e:
        return ChatResponse(
            response=f"Ocorreu um erro interno: {str(e)}. Tente novamente.",
            status="error",
        )


@app.get("/health")
async def health_check():
    """Health check para monitoramento."""
    return {"status": "ok", "service": "ajudante-prof-rodrigo"}

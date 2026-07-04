# 🐉 Ajudante do desenvolvedor Nathanael Jorge — Dragon Ball Super AI Agent

> Agente de IA conversacional especialista no universo de Dragon Ball Super.  
> Projeto acadêmico — Matrícula: **2024206510025**

## 🔗 Acesso

**🌐 Link de produção:** `https://ajudante-prof-rodrigo.onrender.com`

---

## 📋 Funcionalidades

- 🔍 **Consulta de personagens** — Busca informações de 44 personagens por ID (1-44)
- 📊 **Salvamento em planilha** — Grava dados no Google Sheets automaticamente
- 📧 **Envio por e-mail** — Envia dossiê do personagem para qualquer endereço
- 💬 **Chat inteligente** — Interface conversacional com memória de contexto
- ✅ **Validação rigorosa** — Aceita somente IDs válidos (inteiros de 1 a 44)

---

## 🏗️ Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python + FastAPI |
| LLM | OpenAI GPT-4o-mini (Function Calling) |
| Frontend | HTML5 + CSS3 + JavaScript |
| Planilha | Google Sheets API (gspread) |
| E-mail | Gmail SMTP |
| Deploy | Render (Free Tier) |

---

## 🚀 Executar Localmente

### Pré-requisitos

- Python 3.11+
- Conta OpenAI com créditos
- Google Service Account configurada
- Gmail com App Password

### Setup

```bash
# 1. Clonar repositório
git clone <url-do-repo>
cd ajudante-prof-rodrigo

# 2. Criar ambiente virtual
python -m venv .venv
.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
# Copie .env.example para .env e preencha com suas credenciais

# 5. Rodar
uvicorn app.main:app --reload --port 8000
```

Acesse: **http://localhost:8000**

---

## 📁 Estrutura do Projeto

```
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI — rotas e static files
│   ├── agent.py       # Agente OpenAI com Function Calling
│   ├── tools.py       # Tools: buscar, planilha, e-mail
│   ├── prompts.py     # System prompt do agente
│   └── config.py      # Configuração de ambiente
├── static/
│   ├── index.html     # Interface do chat
│   ├── style.css      # Estilos (dark theme)
│   └── app.js         # Lógica do frontend
├── requirements.txt
├── render.yaml        # Config de deploy Render
└── README.md
```

---

## 🔐 Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `OPENAI_API_KEY` | Chave da API OpenAI |
| `GMAIL_USER` | E-mail do Gmail para SMTP |
| `GMAIL_APP_PASSWORD` | Senha de App do Gmail |
| `GOOGLE_CREDENTIALS` | JSON da Service Account (string) |
| `SPREADSHEET_NAME` | Nome da planilha Google Sheets |

---

## 👨‍🏫 Autor

**Jorge** — Matrícula 2024206510025  
Disciplina: Desenvolvimento Mobile  
Professor: Rodrigo

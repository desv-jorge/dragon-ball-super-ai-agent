# 🐉 Ajudante do desenvolvedor Nathanael Jorge — Dragon Ball Super AI Agent

> Agente de IA conversacional especialista no universo de Dragon Ball Super.  
> Projeto acadêmico — Matrícula: **2024206510025**

---

## 📋 Funcionalidades

- 🔍 **Consulta de personagens** — Busca informações de 44 personagens por ID (1-44).
- 📊 **Salvamento em planilha** — Grava os dados consultados no Google Sheets automaticamente.
- 📧 **Envio por e-mail** — Envia um dossiê com HTML formatado e imagens usando automação via Webhook.
- 💬 **Chat inteligente** — Interface conversacional com memória de contexto em LLM.
- ✅ **Validação rigorosa** — Aceita somente IDs válidos (inteiros de 1 a 44) antes de chamar a API.

---

## 🏗️ Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| **Backend** | Python + FastAPI |
| **LLM** | OpenAI GPT-4o-mini (Function Calling) |
| **Frontend** | HTML5 + CSS3 + JavaScript |
| **Planilha** | Google Sheets API (gspread) |
| **Automação de E-mail**| n8n (Integração por Webhook) + Gmail |
| **Deploy** | Render (Free Tier) |

---

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
- Python 3.11+ instalado.
- Conta na OpenAI (com créditos e API Key gerada).
- Google Service Account configurada (arquivo `.json`).
- Conta no [n8n](https://n8n.io/) para gerenciar o disparo de e-mails.

### 2. Setup do Projeto
Clone o repositório e crie um ambiente virtual:
```bash
git clone https://github.com/desv-jorge/dragon-ball-super-ai-agent.git
cd dragon-ball-super-ai-agent

# Windows
python -m venv .venv
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente (.env)
Existe um arquivo de exemplo chamado `.env.example` na raiz do projeto. 
Renomeie uma cópia dele para `.env` e preencha com seus dados:

```env
OPENAI_API_KEY=sk-proj-sua-chave-aqui
SPREADSHEET_NAME=Sua_Planilha_Criada_No_Drive
GOOGLE_CREDENTIALS_FILE=seu-arquivo-de-credenciais.json
```
*(Lembre-se de não subir o `.env` nem o seu `.json` da Service Account para o GitHub! O arquivo `.gitignore` já está configurado para te proteger disso).*

### 4. Rodando o servidor
```bash
uvicorn app.main:app --reload --port 8000
```
Acesse a aplicação no navegador via **http://localhost:8000**.

---

## ⚙️ Configurando o Envio de E-mails (n8n)

Para burlar os bloqueios de portas SMTP de hospedagens gratuitas (como o Render), este projeto usa um **Webhook do n8n** para disparar e-mails. O arquivo de configuração já está pronto para você importar!

1. Crie uma conta ou abra a sua instância do n8n.
2. Crie um novo workflow vazio.
3. No canto superior direito, vá nas opções e escolha **Import from File...**
4. Importe o arquivo **`n8n-workflow-email.json`** (que está na raiz desse repositório).
5. O n8n importará dois nós: um gatilho de Webhook e uma ação de envio pelo Gmail.
6. Clique no nó do **Gmail** e crie uma nova credencial usando sua conta de e-mail (basta seguir as instruções da tela via OAuth2 ou App Password).
7. Mude a chavinha do workflow no canto superior direito para **Active**.
8. (Opcional) Verifique se a *Production URL* do seu webhook bate com a que está definida na função `enviar_email` dentro de `app/tools.py`.

A partir de agora, quando a Inteligência Artificial decidir enviar um e-mail, fará um POST nesse webhook, e o seu n8n se encarregará do envio!

---

## ☁️ Deploy no Render

Para colocar sua aplicação no ar usando o plano gratuito do [Render](https://render.com/):

1. Conecte sua conta do GitHub no Render e selecione a opção **New Web Service**.
2. Escolha o repositório deste projeto.
3. As configurações básicas serão lidas automaticamente a partir do arquivo **`render.yaml`** já incluso no projeto!
4. Na tela de criação do serviço (ou na aba *Environment* depois de criado), vá em **Environment Variables** e adicione:
   - `OPENAI_API_KEY`: A sua chave da OpenAI.
   - `SPREADSHEET_NAME`: O nome da planilha.
5. **Atenção para as Credenciais do Google:**
   Como o Render precisa do arquivo `.json` mas não subimos arquivos sensíveis para o Git, você deve ir na aba **Secret Files** no painel do Render, criar um arquivo (ex: `google-creds.json`) e colar todo o conteúdo da sua Service Account lá dentro.
   Em seguida, adicione uma Environment Variable chamada `GOOGLE_CREDENTIALS_FILE` com o nome desse arquivo gerado (ex: `google-creds.json`).
6. Clique em Deploy e aguarde a finalização.

---

## 👨‍🏫 Autor

**Nathanael Jorge** — Matrícula 2024206510025  
Disciplina: Desenvolvimento Mobile  
Professor: Rodrigo

"""Agente conversacional — OpenAI com Function Calling."""

import json
from openai import AsyncOpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.prompts import SYSTEM_PROMPT
from app.tools import TOOLS_SCHEMA, execute_tool

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Armazena histórico por session_id (em memória — suficiente para demo)
_sessions: dict[str, list[dict]] = {}

MAX_TOOL_ROUNDS = 5  # Limite de ciclos de tool calling por mensagem


def _get_history(session_id: str) -> list[dict]:
    """Retorna ou inicializa o histórico de uma sessão."""
    if session_id not in _sessions:
        _sessions[session_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return _sessions[session_id]


async def chat(session_id: str, user_message: str) -> str:
    """Processa uma mensagem do usuário e retorna a resposta do agente.

    Implementa o loop de Function Calling:
      1. Envia mensagens ao LLM com tools disponíveis.
      2. Se o LLM pedir tool_calls, executa e devolve o resultado.
      3. Repete até o LLM dar uma resposta final (sem tool_calls).
    """
    history = _get_history(session_id)
    history.append({"role": "user", "content": user_message})

    for _ in range(MAX_TOOL_ROUNDS):
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=history,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
            temperature=0.7,
            max_tokens=2048,
        )

        message = response.choices[0].message

        # Adiciona a mensagem do assistente ao histórico
        history.append(message.model_dump())

        # Se não tem tool_calls, é a resposta final
        if not message.tool_calls:
            return message.content or ""

        # Executar cada tool_call
        for tool_call in message.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            result = await execute_tool(fn_name, fn_args)

            # Adiciona o resultado da tool ao histórico
            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

    # Fallback caso exceda o limite de rounds
    return "Desculpe, algo deu errado no processamento. Tente novamente! 😅"

"""GeminiProvider — implementação real do AIProvider via SDK do Google GenAI."""
from __future__ import annotations
from google import genai
from google.genai import types
from src.models.conversation import Message

class GeminiProvider:
    def __init__(self, gcp_project_id: str, gcp_region: str, model: str) -> None:
        # O cliente 'genai.Client' lê automaticamente as credenciais do seu Docker
        self._client = genai.Client(vertexai=True,project=gcp_project_id, location=gcp_region)
        self._model = model

    async def generate_reply(
        self, system_prompt: str, history: list[Message],
    ) -> str:

        # Converte o histórico de mensagens para o formato aceito pelo Gemini
        gemini_contents = [
            types.Content(
                role="user" if msg.sender == "user" else "model",
                parts=[types.Part.from_text(text=msg.content)]
            )
            for msg in history
        ]

        # Configura o System Prompt (Instruções do sistema)
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=1024
        )

        # Executa a chamada de forma assíncrona (usando o cliente .aio)
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=gemini_contents,
            config=config
        )

        return response.text

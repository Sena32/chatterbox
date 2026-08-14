"""GeminiProvider — implementação real do AIProvider via SDK do Google GenAI."""
from __future__ import annotations

from collections.abc import AsyncIterator

from google import genai
from google.genai import types

from src.models.conversation import Message


class GeminiProvider:
    def __init__(self, gcp_project_id: str, gcp_region: str, model: str) -> None:
        self._client = genai.Client(
            vertexai=True, project=gcp_project_id, location=gcp_region
        )
        self._model = model

    def _build_contents(self, history: list[Message]) -> list[types.Content]:
        return [
            types.Content(
                role="user" if msg.sender == "user" else "model",
                parts=[types.Part.from_text(text=msg.content)],
            )
            for msg in history
        ]

    async def generate_reply(
        self, system_prompt: str, history: list[Message],
    ) -> str:
        gemini_contents = self._build_contents(history)
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            max_output_tokens=1024,
        )
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=gemini_contents,
            config=config,
        )
        return response.text

    async def generate_reply_stream(
        self,
        system_prompt: str,
        history: list[Message],
    ) -> AsyncIterator[str]:
        full_text = await self.generate_reply(system_prompt, history)
        if not full_text:
            return
        parts = full_text.split(" ")
        for index, word in enumerate(parts):
            chunk = word if index == 0 else f" {word}"
            yield chunk

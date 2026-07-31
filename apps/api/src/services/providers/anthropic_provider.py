"""AnthropicProvider — implementação real do AIProvider via SDK Anthropic."""

from __future__ import annotations

from anthropic import AnthropicVertex

from src.models.conversation import Message


class AnthropicProvider:
    def __init__(self, gcp_project_id: str,region: str, model: str) -> None:
        self._client = AnthropicVertex(project_id=gcp_project_id,region=region)
        self._model = model

    async def generate_reply(
        self,
        system_prompt: str,
        history: list[Message],
    ) -> str:
        response = await self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": msg.sender if msg.sender == "user" else "assistant", "content": msg.content}
                for msg in history
            ],
        )
        return response.content[0].text

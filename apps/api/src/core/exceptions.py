"""Exceções de domínio — traduzidas para HTTP apenas nos controllers."""


class ConversationNotFoundError(Exception):
    """Conversa não encontrada."""

    def __init__(self, conversation_id: str) -> None:
        self.conversation_id = conversation_id
        super().__init__(f"Conversation not found: {conversation_id}")


class AIProviderError(Exception):
    """Erro ao comunicar com o provedor de IA."""


class AIUnavailableError(Exception):
    """Provedor de IA indisponível; mensagem do usuário já foi persistida."""

    def __init__(self, conversation_id: str) -> None:
        self.conversation_id = conversation_id
        super().__init__(f"AI provider unavailable for conversation: {conversation_id}")

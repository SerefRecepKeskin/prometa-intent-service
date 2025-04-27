from typing import AnyStr, List, Dict, TypedDict
from llama_index.core.base.llms.types import ChatMessage, MessageRole


class ChatMessageFormatter:
    def __init__(self, system_prompt: AnyStr):
        self.system_prompt = system_prompt

    def _format_conversation(self, conversation_data: List) -> str:
        """
        Convert conversation messages into formatted text for analysis

        :param conversation_data: List of Message objects containing conversation messages
        :return: Formatted conversation text
        """
        formatted_text = "=== Conversation Analysis Request ===\n\n"
        
        for msg in conversation_data:
            role = msg.role.capitalize()
            message = msg.message
            formatted_text += f"{role}: {message}\n"
        
        formatted_text += "\n=== End of Conversation ===\n"
        return formatted_text

    def format_messages(
        self,
        conversation_data: List
    ) -> List[ChatMessage]:
        """
        Format all messages for the LLM including system prompt and conversation data

        :param conversation_data: Message objects containing conversation messages
        :return: List of formatted chat messages
        """
        formatted_messages = []

        # Add system prompt
        formatted_messages.append(ChatMessage(
            role=MessageRole.SYSTEM,
            content=self.system_prompt
        ))

        # Add conversation data
        if conversation_data:
            conversation_text = self._format_conversation(conversation_data)
            formatted_messages.append(ChatMessage(
                role=MessageRole.USER,
                content=conversation_text
            ))
        return formatted_messages

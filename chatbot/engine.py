from typing import AnyStr, AsyncGenerator, List, Optional, Dict

from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.base.response.schema import StreamingResponse
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.chat_engine.types import AgentChatResponse

from prompt import SYSTEM_PROMPT

from .message import ChatMessageFormatter


class CustomChatEngine(SimpleChatEngine):

    async def achat(
        self,
        conversation_data: Dict,
    ) -> AgentChatResponse:
        """
        Analyze conversation data

        :param conversation_data: JSON containing conversation messages
        :return: analysis response from gemini server
        """
        formatter = ChatMessageFormatter(
            system_prompt=SYSTEM_PROMPT
        )

        # format messages for sending to llm
        messages = formatter.format_messages(
            conversation_data=conversation_data
        )

        # Use the parent class's llm property to access the LLM
        response = await self._llm.achat(
            messages=messages
        )

        return response

import json
from typing import AnyStr, Dict
from llama_index.core import Settings
from config import config
from util.client import GeminiClient
from .engine import CustomChatEngine

class ChatbotWorker():
    def __init__(self):
        # chat engine for processing prompts
        self.chat_engine = None


    async def _initialize(self) -> None:
        try:

            # create and initialize the language model client
            llm = GeminiClient()

            # set global settings for llama_index
            Settings.llm = llm

            # build the chat engine
            self.chat_engine = CustomChatEngine.from_defaults()
        except Exception as e:
            raise RuntimeError(
                f'Failed to initialize ChatbotWorker: {str(e)}'
            ) from e

    @classmethod
    async def create(cls) -> "ChatbotWorker":
        """
        Create chatbot worker

        :return: ChatbotWorker instance
        """
        # instantiate the class
        instance = cls()

        # perform asynchronous initialization
        await instance._initialize()

        return instance
    

    async def process_prompt_async(
        self,
        messages: Dict
    ) -> Dict[AnyStr, AnyStr]:
        # get response by user message and chat history
        result = await self.chat_engine.achat(
            messages
        )

        assistant_message = result.message.blocks[0].text

        return {'response': assistant_message }
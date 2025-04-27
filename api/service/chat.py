from typing import AnyStr, List, Dict, Any
from uuid import UUID
import json
import httpx
from api.exception import ChatResponseError
from api.schema import Message, MessageResult, AnalysisItem
from chatbot.worker import ChatbotWorker
from util import logger
from config import config  


class ChatService:
    def __init__(self, chatbot: ChatbotWorker = None):
        self._chatbot = chatbot

    async def create_bot_response(
        self,
        messages: List[Message],
        session_identifier: UUID
    ) -> MessageResult:
        """
        Generates a bot response to a conversation in a specific session

        :param messages: list of messages in the conversation
        :param session_identifier: unique identifier for the conversation session
        :return: the bot's response as a "MessageResult" object
        """
        try:
            response = await self._chatbot.process_prompt_async(
                messages=messages
            )
            
            # Parse the analysis from the response
            analysis_items = []
            try:
                analysis_data = json.loads(response['response'])
                if 'analysis' in analysis_data and isinstance(analysis_data['analysis'], list):
                    for item in analysis_data['analysis']:
                        analysis_items.append(
                            AnalysisItem(
                                role=item.get('role', ''),
                                sentence=item.get('sentence', ''),
                                sentiment=item.get('sentiment', ''),
                                intent=item.get('intent', '')
                            )
                        )
            except (json.JSONDecodeError, KeyError, TypeError) as err:
                logger.warning(f"Failed to parse analysis: {err}")
                
            result = MessageResult(
                bot_message=response['response'],
                session_id=session_identifier,
                analysis=analysis_items
            )

            # Log the conversation
            await self._async_log_message(messages, result.bot_message, result.session_id, analysis_items)

            return result

        except Exception as ex:
            logger.error('Unexpected error while creating bot response: %s', ex)
            raise ChatResponseError(
                detail='Failed to create bot response'
            ) from ex

    async def _async_log_message(
        self, 
        messages: List[Message],
        bot_message: str, 
        session_identifier: UUID,
        analysis: List[AnalysisItem] = None
    ) -> None:
        """
        Asynchronously logs the chat messages to the logging service.

        :param messages: The list of messages in the conversation
        :param bot_message: The bot's response to the user
        :param session_identifier: The session identifier for logging purposes
        :param analysis: The analysis items generated for the conversation
        """
        try:
            # Create simplified log payload
            log_data = {
                "session_id": str(session_identifier),
                "analysis": []
            }
            
            # Add analysis items to payload
            if analysis:
                log_data["analysis"] = [
                    {
                        "role": item.role,
                        "sentence": item.sentence,
                        "sentiment": item.sentiment,
                        "intent": item.intent
                    } for item in analysis
                ]
                
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(
                    url=f"{config.logging_service_url}/api/v1/log/save",
                    json=log_data
                )
                response.raise_for_status()
                logger.info(f"Message successfully logged, status code: {response.status_code}")
        except httpx.HTTPStatusError as status_err:
            logger.warning(f"HTTP error while logging message: {status_err.response.status_code}")
        except httpx.RequestError as req_ex:
            logger.warning(f"Request error while logging message: {req_ex}")
        except Exception as log_ex:
            logger.warning('Failed to log message asynchronously: %s', log_ex)

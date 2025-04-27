from typing import Annotated

from fastapi import APIRouter, Depends, Request, Header
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from api.schema import  ConversationRequest
from api.service import ChatService
from api.service.auth import AuthService
from chatbot.worker import ChatbotWorker
from util import logger

chat_router = APIRouter(prefix='/chat')


async def get_chatbot_worker(request: Request) -> ChatbotWorker:
    """
    Initialize chatbot worker once when the application is up
    """
    return request.app.state.chatbot_worker


async def verify_api_key(x_api_key: Annotated[str, Header()]) -> str:
    """
    Verify the API key from request header.
    
    Args:
        x_api_key: API key from request header
    
    Returns:
        str: Verified API key
    
    Raises:
        HTTPException: If API key is invalid
    """
    AuthService.check_auth(x_api_key)
    return x_api_key


@chat_router.post('/analyze')
async def message_route(
    token: Annotated[str, Depends(verify_api_key)],
    conversation: ConversationRequest,
    chatbot_worker: ChatbotWorker = Depends(get_chatbot_worker)
) -> JSONResponse:
    """
    Processes the user's message and returns a bot response

    :param token: token dependency
    :param conversation: incoming conversation request body
    :param chatbot_worker: chatbot worker dependency
    :return: JSONResponse that includes MessageResult
    """
    service = ChatService(chatbot_worker)

    result = await service.create_bot_response(
        messages=conversation.messages,
        session_identifier=conversation.session_identifier
    )

    return JSONResponse(content=jsonable_encoder(result))

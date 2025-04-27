from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.route import chat_router
from chatbot.worker import ChatbotWorker
from config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.chatbot_worker = await ChatbotWorker.create()
    yield

app = FastAPI(lifespan=lifespan)

origins = [config.ui.url]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

prefix = f'/api/{config.app.version}'

app.include_router(chat_router, prefix=prefix)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=config.app.port
    )

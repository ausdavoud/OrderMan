from contextlib import asynccontextmanager

from aiogram.types import Update
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from utils import get_bot, get_dispatcher

load_dotenv()

bot = None
dispatcher = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global bot, dispatcher
    print("[*] Setting Bot, Webhook and Dispatcher ...")
    bot = await get_bot()
    dispatcher = get_dispatcher()

    yield


app = FastAPI(lifespan=lifespan)


@app.post("/open")
async def http_handler(request: Request):
    request_json = await request.json()
    update = Update.model_validate(request_json)
    print(f"Text Message: {update.message.text}")
    response = await dispatcher.feed_update(bot=bot, update=update)

    return str(response)


@app.get("/")
async def get_webhook_url(request: Request):
    info = await bot.get_webhook_info()
    return {"webhook url": info.url}

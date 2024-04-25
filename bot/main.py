from contextlib import asynccontextmanager

from aiogram.types import Update
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from utils import get_bot, get_dispatcher, set_webhook

load_dotenv()

bot, dispatcher = None, None


@asynccontextmanager
async def lifetime(app: FastAPI):
    global bot, dispatcher
    bot = await get_bot()
    dispatcher = get_dispatcher()

    print("[*] Set webhook url triggered ...")
    await set_webhook(bot=bot)

    yield


app = FastAPI(lifetime=lifetime)


@app.post("/open")
async def http_handler(request: Request):
    request_json = await request.json()
    update = Update.model_validate(request_json)
    print(f"Text Message: {update.message.text}")
    response = await dispatcher.feed_raw_update(bot=bot, update=request_json)

    return str(response)


@app.get("/")
async def get_webhook_url(request: Request):
    info = await bot.get_webhook_info()
    return {"webhook url": info.url}

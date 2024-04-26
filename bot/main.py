from contextlib import asynccontextmanager

from aiogram.types import Update
from loggers import BotLogger
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from utils import get_bot, get_dispatcher

load_dotenv()


logging = BotLogger(__name__)

bot = None
dispatcher = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global bot, dispatcher
    logging.info("Setting Bot, Webhook and Dispatcher")
    bot = await get_bot()
    dispatcher = get_dispatcher()
    logging.info("Bot and Dispatcher were set")

    yield

    await bot.delete_webhook()
    logging.info("Webhook deleted")

    await bot.close()
    logging.info("Bot closed")

    
app = FastAPI(lifespan=lifespan)


@app.post("/open")
async def http_handler(request: Request):
    logging.info("Message Received")
    request_json = await request.json()
    logging.info("Converting json to Pydantic Update")
    update = Update.model_validate(request_json)
    logging.info(f"Text Message: {update.message.text}")
    logging.info("Sending answer")
    response = await dispatcher.feed_update(bot=bot, update=update)
    logging.info("Answer was sent")
    return str(response)


@app.get("/")
async def get_webhook_url(request: Request):
    logging.info("Fetching webhook info")
    info = await bot.get_webhook_info()
    return {"webhook url": info.url}

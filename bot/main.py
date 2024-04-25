import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from handlers import setup_handlers
from __init__ import set_bot_commands


load_dotenv()

# Initialize fastapi application
bot_key = os.getenv("TELEGRAM_BOT_TOKEN") or ""
print(bot_key)
bot_url = "https://api.telegram.org/bot{token}".format(token=bot_key)

bot = Bot(token=bot_key, parse_mode='HTML')
dispatcher = Dispatcher()
setup_handlers(dispatcher)

@asynccontextmanager
async def lifetime(app: FastAPI):
    await set_bot_commands(bot=bot)

    yield

app = FastAPI(lifetime=lifetime)

###########################################################################
# POST-Method for TELEGRAM-Webhook
@app.post("/open")
async def http_handler(request: Request):
    response_text, user_identity = None, None
    
    update = Update.model_validate(await request.json())
    print(f"Update Text: {update.message.text}")
    await dispatcher.feed_raw_update(bot, await request.json())
    # Try parsing and handling text messages from telegram bot-api
    try:
        # Parse input message from JSON body
        incoming_data = await request.json()
        print("[*] Incoming POST request:",incoming_data)
        # Extract required values from input message
        user_identity = incoming_data['message']['chat']['id']
        message_text = incoming_data['message']['text']
        # Execute handler function for text messages
        response_text = handle_message(message_text)
    
    # Handle errors
    except Exception as e:
        response_text = "Sorry! I could not handle your last message properly!"
    
    print("[*] Response message:",user_identity,"=>",response_text)
    # Send response message
    return {"method": "sendMessage","text": response_text,"chat_id": user_identity}


def handle_message(message_text: str) -> str:
    """
        TODO: This function can be extended. You can apply any logic you like!
    """
    # Send greetings on '/start' message
    if message_text == "/start": return "Hello User!"
    # Otherwise simply repeat the input message
    else: return message_text



###########################################################################
# GET-Method for setting TELEGRAM webhook URL
@app.get("/")
async def set_webhook_url(request: Request):
    print("[*] Set webhook url triggered ...")
    bot = Bot(token=bot_key)
    HOST = os.getenv("DETA_SPACE_APP_HOSTNAME")
    # HOST = "tel_tbot_based-1-x2228392.deta.app"

    webhook_url = f"https://{HOST}/open"
    await bot.set_webhook(webhook_url)

    info = await bot.get_webhook_info()
    return {"webhook url": info.url}

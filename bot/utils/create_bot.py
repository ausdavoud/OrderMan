import os

from __init__ import set_bot_commands
from aiogram import Bot, Dispatcher
from handlers import setup_handlers
from loggers import BotLogger

logger = BotLogger(__name__)


class TokenException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_token() -> str:
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        raise TokenException("Invalid Bot Token.")

    return TOKEN


async def get_bot() -> Bot:
    TOKEN = get_token()
    bot = Bot(token=TOKEN, parse_mode="HTML")
    await set_bot_commands(bot=bot)
    await set_webhook(bot=bot)
    return bot


def get_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    setup_handlers(dispatcher)

    return dispatcher


async def set_webhook(bot: Bot):
    HOST = os.getenv("DETA_SPACE_APP_HOSTNAME")

    webhook_url = f"https://{HOST}/open"

    webhook_info = await bot.get_webhook_info()

    if webhook_url != webhook_info.url:
        logger.info(f"Webhook is already set to {webhook_info.url}")
    else:
        await bot.set_webhook(webhook_url)
        webhook_info_after_set = await bot.get_webhook_info()
        logger.info(f"Webhook was set to {webhook_info_after_set.url}")

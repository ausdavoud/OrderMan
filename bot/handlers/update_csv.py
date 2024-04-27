import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiohttp import ClientSession
from loggers import BotLogger

logging = BotLogger(__name__)

router = Router()


@router.message(Command("update_csv"))
async def command_start(message: Message, state: FSMContext) -> None:
    HOST = os.getenv("DETA_SPACE_APP_HOSTNAME")
    # HOST = "tbotmain-1-v6789165.deta.app"
    update_csv_url = f"https://{HOST}/deta/update_csv"
    # update_csv_url = "http://localhost:4200/update_csv"
    async with ClientSession() as session:
        async with session.get(update_csv_url) as response:
            result = await response.json()
            logging.info(f"update csv result: {result = }")
            if result["result"] == "ok":
                await message.answer("فایل ها اپدیت شدند!")

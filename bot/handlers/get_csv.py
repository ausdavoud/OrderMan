import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, Message
from aiohttp import ClientSession
from dotenv import load_dotenv
from loggers import BotLogger

load_dotenv(override=True)

logging = BotLogger(__name__)

router = Router()


@router.message(Command("get_csv"))
async def command_start(message: Message, state: FSMContext) -> None:
    logging.info("Entered commands handler -> /get_csv")

    HOST = os.getenv("DETA_SPACE_APP_HOSTNAME")
    get_items_url = f"https://{HOST}/deta/get_breads_csv"
    get_breads_url = f"https://{HOST}/deta/get_items_csv"
    async with ClientSession() as session:
        async with session.get(get_items_url) as response:
            logging.info("sending post request to /get_items_csv")

            response_json = await response.json()

            logging.info(f"{response_json = }")
            csv_name = response_json["file_name"]
            if csv_name is not None:
                csv_binary = response_json["content"]["path"]
                csv_binary = csv_binary.encode("utf-8")
                telegram_file = BufferedInputFile(file=csv_binary, filename=csv_name)
                await message.answer_document(telegram_file)
            else:
                await message.answer("فایل کل سفارش ها یافت نشد. ابتدا آپدیت کنید.")

        async with session.get(get_breads_url) as response:
            logging.info("Sent post request to /get_breads_csv")

            response_json = await response.json()

            logging.info(f"Received response as json: {response_json}")
            csv_name = response_json["file_name"]
            if csv_name is not None:
                csv_binary = response_json["content"]["path"]
                csv_binary = csv_binary.encode("utf-8")
                telegram_file = BufferedInputFile(file=csv_binary, filename=csv_name)
                await message.answer_document(telegram_file)
            else:
                await message.answer("فایل نان ها یافت نشد. ابتدا آپدیت کنید.")

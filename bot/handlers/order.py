import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiohttp import ClientSession
from core import deta_result_to_message, order_dict_to_message, orders_from_text
from loggers import BotLogger

logging = BotLogger(__name__)

router = Router()


class OrderStates(StatesGroup):
    get_order = State()
    confirm_order = State()


@router.message(Command("order"))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderStates.get_order)
    send_order_message = await message.answer(
        "سفارش خود را در فرمت تعیین شده ارسال کنید:", reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(send_order_message=send_order_message)


@router.message(OrderStates.get_order)
async def process_order(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderStates.confirm_order)
    data = await state.update_data(order=message.text)
    order = data["order"]
    try:
        items_dict, breads_dict = orders_from_text(order)
    except ValueError:
        logging.error(f"Probably a float conversion error\n{order}")
    logging.info("Items converted to dict successfully.")
    await state.update_data(items_dict=items_dict)
    await state.update_data(breads_dict=breads_dict)

    text = order_dict_to_message(items_dict)
    last_message = await message.answer(
        text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="بله"), KeyboardButton(text="خیر")]]
        ),
    )
    await data["send_order_message"].delete()
    await state.update_data(last_message=last_message)


@router.message(OrderStates.confirm_order)
async def confirm_order(message: Message, state: FSMContext) -> None:
    data = await state.update_data(confirm=message.text)
    await state.clear()
    logging.info("Received confirmation.")

    HOST = os.getenv("DETA_SPACE_APP_HOSTNAME")
    # HOST = "tbotmain-1-v6789165.deta.app"
    post_items_url = f"https://{HOST}/deta/put_items"
    post_breads_url = f"https://{HOST}/deta/put_breads"
    items_dict = data["items_dict"]
    breads_dict = data["breads_dict"]
    last_message: Message = data["last_message"]
    items_dict["csv"] = False
    breads_dict["csv"] = False

    logging.info("dicts are ready to be sent.")

    result = ""
    if data["confirm"] == "بله":
        async with ClientSession() as session:
            async with session.post(post_items_url, json=items_dict) as response:
                if response.ok:
                    logging.info("dict were put to Items DetaBase")
                result = await response.json()
                result = deta_result_to_message(result)
                logging.info(result)

            async with session.post(post_breads_url, json=breads_dict) as response:
                logging.info("dicts were put to Breads DetaBase")
                bread_result = await response.json()
                logging.info(f"Type of result from deta: {type(result)}")

        logging.info(f"{last_message = }")
        await message.answer(result, reply_markup=ReplyKeyboardRemove())
    elif data["confirm"] == "خیر":
        await message.answer("سفارش را تایید نکردید!", reply_markup=ReplyKeyboardRemove())

    await last_message.delete()
    await message.delete()
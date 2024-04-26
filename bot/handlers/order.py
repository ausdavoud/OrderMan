from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from core import orders_from_text
import os
from aiohttp import ClientSession
from loggers import BotLogger


logging = BotLogger(__name__)

router = Router()


class OrderStates(StatesGroup):
    get_order = State()
    confirm_order = State()


@router.message(Command("order"))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderStates.get_order)
    await message.answer("Hey, I am ready to receive your order...")


@router.message(OrderStates.get_order)
async def process_order(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderStates.confirm_order)
    data = await state.update_data(order=message.text)
    order = data["order"]
    try:
        items_dict, breads_dict = orders_from_text(order)
    except ValueError as e:
        logging.error(f"Probably a flaot conversion error\n{order}")
    logging.info("Items converted to dict successfully.")
    await state.update_data(items_dict=items_dict)
    await state.update_data(breads_dict=breads_dict)

    text = f"{str(items_dict)}.\n you confirm?(yes/no)"
    await message.answer(text)


@router.message(OrderStates.confirm_order)
async def confirm_order(message: Message, state: FSMContext) -> None:
    data = await state.update_data(confirm=message.text)
    await state.clear()
    logging.info("Received confirmation.")

    HOST = os.getenv("DETA_SPACE_APP_HOSTNAME")
    HOST = "tbotmain-1-v6789165.deta.app"
    post_items_url = f"https://{HOST}/deta/put_items"
    post_breads_url = f"https://{HOST}/deta/put_breads"
    items_dict = data["items_dict"]
    breads_dict = data["breads_dict"]

    logging.info("dicts are ready to be sent.")

    
    if data["confirm"] == "yes":
        async with ClientSession() as session:
            async with session.post(post_items_url, json=items_dict) as response:
                if response.ok:
                    logging.info("dict were put to Items DetaBase")
                result = await response.text()
                logging.info(result)
                await message.answer(result)

            async with session.post(post_breads_url, json=breads_dict) as response:
                logging.info("dicts were put to Breads DetaBase")
                result = await response.text()
                logging.info(result)
                await message.answer(result)

        

    elif data["confirm"] == "no":
        await message.answer("Order was canceled.")

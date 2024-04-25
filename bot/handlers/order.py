from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

router = Router()


class OrderStates(StatesGroup):
    order = State()


@router.message(Command("order"))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(OrderStates.order)
    await message.answer("Hey, I am ready to receive your order...")


@router.message(OrderStates.order)
async def process_order(message: Message, state: FSMContext) -> None:
    data = await state.update_data(order=message.text)
    await state.clear()
    order = data["order"]
    await message.answer(f"Your order was: {order}")

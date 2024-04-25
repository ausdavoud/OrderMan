from aiogram import Dispatcher

from . import (
    order
)

def setup_handlers(dp: Dispatcher):
    dp.include_routers(
        order.router
    )
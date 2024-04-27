from aiogram import Dispatcher

from . import order, get_csv, update_csv


def setup_handlers(dp: Dispatcher):
    dp.include_routers(order.router, get_csv.router, update_csv.router)

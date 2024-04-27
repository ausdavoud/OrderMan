from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

bot_commands = [
    ("order", "Make a new order"),
    ("get_csv", "Get last csv files (sheets)"),
    ("update_csv", "Update the csv files (sheets)")
]


async def set_bot_commands(bot: Bot):
    wrapped_commands = list(
        BotCommand(command="/" + cmd, description=text) for cmd, text in bot_commands
    )
    await bot.set_my_commands(wrapped_commands, scope=BotCommandScopeDefault())

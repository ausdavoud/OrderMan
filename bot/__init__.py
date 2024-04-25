from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat

bot_commands = ("order", "Make a new order")


async def set_bot_commands(bot: Bot):
    wrapped_commands = list(
        BotCommand(command="/" + cmd, description=text) for cmd, text in bot_commands
    )
    await bot.set_my_commands(wrapped_commands, scope=BotCommandScopeChat())

import tracemalloc


import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

from src.helpers import config
from src.helpers.functions import get_temperature, get_wind

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)
print("Bot started")


async def set_bot_commands(bot: Bot):
    command1 = BotCommand(command="/start", description="Start the bot")
    command2 = BotCommand(command="/help", description="Get help")
    commands = [command1, command2]
    await bot.set_my_commands(commands)


set_bot_commands(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    print(f"ID {message.from_user.id}")
    if message.from_user.username == 'flooywq':
        await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAG1a2ZkN9xOYG5XJyjY3pvbgCNo5lbh')
    else:
        await message.answer(
            f"Hello {message.from_user.first_name}! It's a weather bot created with aiogram! Enter a city name, "
            f"and I will give you data on the weather in this"
            "city!")
        print(f"First name {message.from_user.first_name}")
        print(f"ID {message.from_user.id}")
        if message.from_user.username:
            print(f"username {message.from_user.username}")



@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    print(f"ID {message.from_user.id}")
    if message.from_user.username == 'flooywq':
        await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAG1a2ZkN9xOYG5XJyjY3pvbgCNo5lbh')
    else:
        await message.answer(f"It's a weather bot created with aiogram! Enter a city name, "
                             f"and I will give you data on the weather in this city!")


@dp.message_handler()
async def get_city(message: types.Message):
    print(f"ID {message.from_user.id}")
    global city
    if message.from_user.username == 'flooywq':
        await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAG1a2ZkN9xOYG5XJyjY3pvbgCNo5lbh')
    else:

        city = message.text
        temp_btn = InlineKeyboardButton(text="Temperature", callback_data="temp")
        wind_btn = InlineKeyboardButton(text="Wind", callback_data="wind")
        keyboard = InlineKeyboardMarkup().add(temp_btn).add(wind_btn)
        await message.reply("Which data you want to get?", reply_markup=keyboard)


@dp.callback_query_handler(text=["temp", "celsius", "fahrenheit", "wind"])
async def callback_query_handler(call: types.CallbackQuery):
    print(f"First name {call.message.from_user.first_name}")
    print(f"ID {call.message.from_user.id}")
    if call.message.from_user.username == 'flooywq':
        await bot.send_sticker(chat_id=call.message.chat.id, sticker='AgADER8AAmJCSEg')
    else:
        if call.message.from_user.username:
            print(f"username {call.message.from_user.username}")
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.API_KEY}&units=metric")
        data = res.json()
        try:
            await get_temperature(call=call, data=data)
        except:
            await call.message.answer('City not found')
        await get_wind(call=call, data=data)


if __name__ == "__main__":
    try:

        executor.start_polling(dp)
    except:
        print('Error')

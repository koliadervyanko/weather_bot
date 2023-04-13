from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def get_temperature(call: types.CallbackQuery, data):
    global temp
    city = data['name']

    if call.data == "temp":
        try:

            temp = round(data['main']['temp'])
            celsius = InlineKeyboardButton(text='Celsius', callback_data='celsius')
            fahrenheit = InlineKeyboardButton(text='Fahrenheit', callback_data='fahrenheit')
            keyboard = InlineKeyboardMarkup().add(celsius).add(fahrenheit)

            await call.message.answer(f"You want to get temperature in: ", reply_markup=keyboard)

        except Exception:
            await call.message.answer('City not found')
            print(Exception)
    if call.data == "celsius":
        try:
            await call.message.answer(f"Now temperature in *{city}* is: *{temp}*℃", parse_mode=types.ParseMode.MARKDOWN)
        except:
            await call.message.answer('Error')
    if call.data == 'fahrenheit':
        try:
            fahrenheit_temp = (temp * 9 / 5) + 32
            await call.message.answer(f"Now temperature in *{city}* is: *{fahrenheit_temp}*℉",
                                      parse_mode=types.ParseMode.MARKDOWN)
        except:
            await call.message.answer('Error')


async def get_wind(call: types.CallbackQuery, data):
    city = data['name']
    if call.data == "wind":
        wind_speed = data["wind"]["speed"]
        wind_deg = data["wind"]["deg"]
        await call.message.answer(f'Now in *{city}* wind speed is: *{wind_speed}*, and deg of wind is: *{wind_deg}*',
                                  parse_mode=types.ParseMode.MARKDOWN)

import os

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram import Router
from dotenv import load_dotenv
load_dotenv()


bot_token = os.getenv('BOT_TOKEN')
weather_token = os.getenv('WEATHER_TOKEN')

storage = MemoryStorage()
bot = Bot(token=bot_token)
dp = Dispatcher(storage=storage)
router = Router()

dp.include_router(router)


@router.message(Command("start"))
async def start(message: types.Message):
    await message.reply("Привет! Введи название города, чтобы узнать погоду:")


@router.message()
async def get_weather(message: types.Message):
    city = message.text
    weather_data = get_weather_data(city)

    if weather_data:
        response = (
            f"Погода в {city}:\n"
            f"Температура: {weather_data['temp']}°C\n"
            f"Влажность: {weather_data['humidity']}%\n"
            f"Описание: {weather_data['description']}"
        )
    else:
        response = "Что-то пошло не так :("

    await message.reply(response)


def get_weather_data(city):
    url = get_url(city)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description']
        }
    return None


def get_url(city: str) -> str:
    return (f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={city}"
            f"&appid={weather_token}"
            f"&units=metric"
            f"&lang=ru")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())

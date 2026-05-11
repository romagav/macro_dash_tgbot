import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from pathlib import Path
from data_pars import get_usd_rate_history, get_key_rate_history
from plot import create_dollar_chart, create_key_rate_chart

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
BOT_TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот-макроаналитик.\n"
        "Показываю актуальные данные по курсу доллара и ключевой ставке ЦБ РФ.\n\n"
        "Команды:\n"
        "/usd — график курса доллара\n"
        "/ks — график ключевой ставки"
    )


@dp.message(Command("usd"))
async def cmd_usd(message: types.Message):
    await message.answer("Строю график курса доллара... Данные ЦБ РФ.")
    try:
        df = get_usd_rate_history(90)
        current = df['rate'].iloc[-1]
        min_rate = df['rate'].min()
        max_rate = df['rate'].max()
        chart = create_dollar_chart(df)
        caption = (
            f"Курс USD/RUB за 90 дней\n"
            f"Текущий: {current:.2f} ₽\n"
            f"Минимум: {min_rate:.2f} ₽\n"
            f"Максимум: {max_rate:.2f} ₽"
        )
        await message.answer_photo(
            types.BufferedInputFile(chart.getvalue(), filename="usd.png"),
            caption=caption
        )
        chart.close()

    except Exception as e:
        await message.answer(f"Ошибка при получении данных: {e}")


@dp.message(Command("ks"))
async def cmd_key_rate(message: types.Message):
    await message.answer("Строю график ключевой ставки... Данные ЦБ РФ.")
    try:
        df = get_key_rate_history(365)
        current = df['rate'].iloc[-1]
        min_rate = df['rate'].min()
        max_rate = df['rate'].max()
        chart = create_key_rate_chart(df)
        caption = (
            f"Ключевая ставка ЦБ РФ за год\n"
            f"Текущая: {current}%\n"
            f"Минимум: {min_rate}%\n"
            f"Максимум: {max_rate}%"
        )
        await message.answer_photo(
            types.BufferedInputFile(chart.getvalue(), filename="key_rate.png"),
            caption=caption
        )
        chart.close()

    except Exception as e:
        await message.answer(f"Ошибка при получении данных: {e}")


async def main():
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
import requests
from decouple import config
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


WEBAPP_URL = config("WEBAPP_URL")
BASE_URL = config("BASE_URL")

router = Router()


def telemtery(message: Message):
    try:
        requests.post(
            url=BASE_URL + "/api/v1/telemetry/",
            data={
                "id": message.from_user.id,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "username": message.from_user.username
            },
        )
    except:
        pass


@router.message(CommandStart())
async def command_start_handler(message: Message):
    telemtery(message)
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Tarix onlayn repetitor (ASTRON)",
            url="https://t.me/tarix_repetitor_astron",
        )
    )
    builder.add(
        InlineKeyboardButton(text="Ilovani ochish", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    builder.adjust(1, 1)
    await message.answer(
        'Assalomu aleykum.\n\n"ASTRON - onlayn repetitor" loyihasining ilovasiga xush kelibsiz!!!\n\n- Ilovadan foydalanish uchun pastgi chap burchakdagi "Ilovani ochish" tugmasiga bosing.\n\n- Murojaat yo\'llash uchun @astron_corp ga yozing.',
        reply_markup=builder.as_markup(),
    )

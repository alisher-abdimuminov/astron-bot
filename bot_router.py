import requests
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton, FSInputFile, MessageReactionUpdated
from aiogram.utils.keyboard import InlineKeyboardBuilder
from decouple import config


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
                "username": message.from_user.username,
            },
        )
    except:
        pass


@router.message(CommandStart())
async def command_start_handler(message: Message):
    telemtery(message)

    photo = FSInputFile("images/starter.jpg")

    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Telegram kanalga a'zo bo'lish",
            url="https://t.me/tarix_repetitor_astron",
        )
    )
    builder.add(
        InlineKeyboardButton(text="Ilovani ochish", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    builder.adjust(1, 1)
    await message.answer_photo(
        photo=photo,
        caption="""Assalomu aleykum!!!

"ASTRON - onlayn repetitor" loyihasining ilovasiga xush kelibsiz!!!

⚜️Tarix fanidan bizda mavjud:
- Yangi testlar
- Bepul savol-javoblar
- Mavzulashgan qo'llanmalar

📲 Murojaat uchun: @astron_corp

📌 Ilovadan foydalanish uchun pastgi chap burchakdagi "Ilovani ochish" tugmasiga bosing.""",
        reply_markup=builder.as_markup(),
    )

@router.message_reaction()
async def handle_reactions(event: MessageReactionUpdated):
	if len(event.new_reaction) <= len(event.old_reaction):
		return

	user = event.user
	if not user:
		return

	user_id = user.id
	chat_id = event.chat.id
	message_id = event.message_id

	print(f"User {user_id} reacted to message {message_id} in chat {chat_id}")

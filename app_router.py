import httpx
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.types import (
    ChatMember,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from decouple import config
from fastapi import APIRouter, Request
from pydantic import BaseModel

BASE_URL = config("BASE_URL")
WEBAPP_URL = config("WEBAPP_URL")

router = APIRouter()


class PostSchema(BaseModel):
    content: str
    post_id: int | str


@router.get("/is-chat-member/")
async def is_chat_member(
    request: Request, user_id: int | str, chat_id: int | str
) -> dict:
    bot: Bot = request.app.state.bot
    try:
        chat_member: ChatMember = await bot.get_chat_member(
            chat_id=chat_id, user_id=user_id
        )
        return {"status": "success", "code": "", "data": chat_member.status}
    except Exception as e:
        return {"status": "error", "code": "chat_not_found", "data": None}


@router.get("/verify-channel")
async def verify_channel(request: Request, channel: int | str) -> dict:
    bot: Bot = request.app.state.bot

    try:
        chat_member: ChatMember = await bot.get_chat_member(
            chat_id=channel, user_id=bot.id
        )
        return {"status": "success", "code": "", "data": chat_member.status}
    except Exception as e:
        return {"status": "error", "code": "chat_not_found", "data": None}


@router.get("/send-message/")
async def send_message(
    request: Request, chat_id: int | str, ads: str | int, content: str
) -> dict:
    bot: Bot = request.app.state.bot

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            await bot.send_message(chat_id=chat_id, text=content)
            await client.get(f"{BASE_URL}/api/v1/increment-receivers/?ads={ads}")
        except Exception as e:
            await client.get(
                f"{BASE_URL}/api/v1/increment-receivers/?ads={ads}&user_id={chat_id}"
            )
            print("Message did not send:", e)

    return {"status": "ok"}


@router.post("/send-post/")
async def send_post(payload: PostSchema, request: Request) -> dict:
    bot: Bot = request.app.state.bot

    button_url = f"https://t.me/astrontest_bot?startapp={payload.post_id}"

    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎁 Bonus",
                    url=button_url,
                )
            ]
        ]
    )

    try:
        message = await bot.send_message(
            chat_id="@test_aaa_bbb",
            text=payload.content,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

        return {
            "status": "success",
            "data": {
                "message_id": message.message_id,
                "chat_id": message.chat.id,
            },
        }
    except Exception as e:
        print(f"Post jo'natishda xatolik: {e}")
        return {"status": "error", "message": str(e)}

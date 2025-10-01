import requests
from aiogram import Bot
from decouple import config
from aiogram.types import ChatMember
from fastapi import APIRouter, Request


BASE_URL = config("BASE_URL")

router = APIRouter()


@router.get("/is-chat-member/")
async def is_chat_member(request: Request, user_id: int | str, chat_id: int | str) -> None:
    bot: Bot = request.app.state.bot
    try:

        chat_member: ChatMember = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)

        return {
            "status": "success",
            "code": "",
            "data": chat_member.status
        }
    except Exception as e:
        return {
            "status": "error",
            "code": "chat_not_found",
            "data": None
        }
    

@router.get("/verify-channel")
async def verify_channel(request: Request, channel: int | str) -> None:
    bot: Bot = request.app.state.bot

    try:
        chat_member: ChatMember = await bot.get_chat_member(chat_id=channel, user_id=bot.id)

        return {
            "status": "success",
            "code": "",
            "data": chat_member.status
        }
    except Exception as e:
        return {
            "status": "error",
            "code": "chat_not_found",
            "data": None
        }
    

@router.get("/send-message/")
async def send_message(request: Request, chat_id: int | str, ads: str | int, content: str):
    bot: Bot = request.app.state.bot

    try:
        await bot.send_message(chat_id=chat_id, text=content)

        requests.get(BASE_URL + f"/increment-receivers/?ads={ads}")

    except Exception as e:
        print("Error:Message did not send.")
        print(e)
    return {
        "status": "ok"
    }

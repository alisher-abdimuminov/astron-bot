import asyncio
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import MenuButtonWebApp, WebAppInfo
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app_router import router as app_router
from bot_router import router as bot_router

TOKEN = config("TOKEN")
WEBAPP_URL = config("WEBAPP_URL")
origins = [
    "http://localhost:3000",
    "https://webapp.astron.uz",
]


async def bot_on_startup(bot: Bot):
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Ilovani ochish",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )
    )


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router=bot_router)
dp.startup.register(bot_on_startup)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Polling'ni alohida task qilib ishga tushiramiz
    polling_task = asyncio.create_task(
        dp.start_polling(
            bot,
            allowed_updates=[
                "message",
                "edited_message",
                "channel_post",
                "message_reaction",
                "message_reaction_updated",
                "callback_query",
            ],
            handle_signals=False,  # <--- MUHIM: Uvicorn va aiogram signallari toqnashmasligi uchun!
        )
    )

    app.state.bot = bot
    yield

    # --- SHUTDOWN (Ctrl+C bosilganda ishlaydigan qism) ---
    # stop_polling() o'rniga birinchi task'ni bekor qilamiz va HTTP seansni yopamiz
    polling_task.cancel()

    try:
        await polling_task
    except (asyncio.CancelledError, Exception):
        pass

    # Bot HTTP klient seansini majburiy yopamiz
    await bot.session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router=app_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

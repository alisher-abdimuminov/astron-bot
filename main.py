import asyncio
import uvicorn
from decouple import config
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from aiogram.types import MenuButtonWebApp, WebAppInfo
from aiogram.client.default import DefaultBotProperties

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
    asyncio.create_task(dp.start_polling(bot))
    app.state.bot = bot
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=app_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if __name__ == "__main__":
#     uvicorn.run(app, port=8080)

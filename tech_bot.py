import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from fastapi import FastAPI, Request

from botcore.middlewars.middlewars import ChatMiddleware
from config import APP_DEBUG, WEBHOOK_URL_TECH, WEBHOOK_PATH_TECH, BOT_TOKEN
from db import session
from storage import storage
from botcore.handlers.tech.tech_handler import router as tech_router
from botcore.handlers.tech.admin_handler import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    bot = create_bot(BOT_TOKEN)
    await bot.set_webhook(WEBHOOK_URL_TECH + BOT_TOKEN)
    yield


app = FastAPI(lifespan=lifespan)


def create_dp():
    dp = Dispatcher(storage=storage, session=session)
    dp.update.middleware(ChatMiddleware())
    dp.include_router(tech_router)
    dp.include_router(admin_router)
    return dp


dp = create_dp()


@app.post(WEBHOOK_PATH_TECH + "{token}")
async def receive_update(request: Request, token: str):
    json_data = await request.json()
    update = types.Update(**json_data)
    bot = create_bot(token)

    try:
        await dp.feed_webhook_update(bot, update)
    except:
        pass

    return {"status": "ok"}


def create_bot(token):
    bot = Bot(token=token, parse_mode=ParseMode.HTML)
    return bot


async def start_bot():
    bot = create_bot(BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if int(APP_DEBUG):
        asyncio.run(start_bot())
    else:
        uvicorn.run(app, host="0.0.0.0")

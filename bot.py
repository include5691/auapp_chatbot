from dotenv import load_dotenv
load_dotenv()

import logging
import os
import logging
import asyncio
import uvicorn
from urllib.parse import quote
from fastapi import FastAPI, Request
from colorama import Fore, Style
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError
from au_b24 import get_leads, update_lead, get_lead, get_user
from e5lib.funcs import phone_purge, create_phone_vars
from e5lib.time import get_yesterday
from aulib.au_engine import get_engines
from _redis import redis_cli

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger('aiogram').setLevel(logging.WARNING)

dp = Dispatcher()
bot = Bot(token=os.getenv("TELEGRAM_BOT_API_TOKEN"))

@dp.message(CommandStart())
async def begin_handler(message: Message) -> None:
    await message.answer(os.getenv("WELCOME_TEXT"))

@dp.message()
async def phone_validation_handler(message: Message) -> None:
    logging.info(message.text)
    phone = phone_purge(message.text)
    if not phone:
        logging.info(f"{Fore.RED}Invalid phone number{Style.RESET_ALL}")
        await message.answer(os.getenv("PHONE_INVALID_TEXT"))
        return
    phone_vars = create_phone_vars(phone, "*")
    if not phone_vars:
        logging.info(f"{Fore.RED}Invalid phone number{Style.RESET_ALL}")
        await message.answer(os.getenv("PHONE_PARSE_INVALID_TEXT"))
        return
    lead = None
    for phone in phone_vars:
        leads = get_leads(filters={"PHONE": phone, ">DATE_CREATE": get_yesterday()}, select=["ID"], order="DESC")
        if leads:
            lead = leads[0]
            break
    if not lead:
        logging.info(f"{Fore.RED}Lead not found{Style.RESET_ALL}")
        await message.answer(os.getenv("LEAD_NOT_FOUND_TEXT"))
        return
    lead_id = lead.get("ID")
    redis_cli.set(lead_id, message.chat.id, ex=86400*7)
    await message.answer(os.getenv("LEAD_FOUND_TEXT").format(lead_id))
    if message.from_user and message.from_user.username:
        update_lead(lead_id, {os.getenv("TELEGRAM_LINK_FIELD_ID"): f"https://t.me/{message.from_user.username}"})
        logging.info(f"{Fore.GREEN}Updated lead {lead_id} with tg username {message.from_user.username}{Style.RESET_ALL}")    

app = FastAPI()

@app.post("/lead")
async def process_distributed_lead(request: Request):
    form = await request.form()
    if not form:
        return
    value = form.get("document_id[2]")
    if not value or not isinstance(value, str):
        return
    lead_id = value.split("_")[1]
    chat_id = redis_cli.get(lead_id)
    if not chat_id:
        return
    lead = get_lead(lead_id)
    if not lead:
        return
    user_id = lead.get("ASSIGNED_BY_ID")
    if not user_id:
        return
    user = get_user(user_id)
    if not user:
        return
    engines = get_engines(user_id)
    if not engines:
        return
    wa_link = os.getenv("WA_API_URL").format(phone=phone_purge(engines[0].wid), text=quote(os.getenv("WA_FIRST_MESSAGE_TEXT")))
    try:
        await bot.send_message(chat_id.decode(), os.getenv("LEAD_DIST_TEXT").format(user.get("NAME"), wa_link))
        logging.info(f"{Fore.LIGHTGREEN_EX}Sent dist text to {lead_id}{Style.RESET_ALL}")
    except TelegramForbiddenError as e:
        logging.error(f"{Fore.RED}TelegramForbiddenError: {e}{Style.RESET_ALL}")

async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=8500, log_level="warning", loop="asyncio")
    server = uvicorn.Server(config)
    server_task = asyncio.create_task(server.serve())
    bot_task = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(bot_task, server_task)

if __name__ == '__main__':
    asyncio.run(main())
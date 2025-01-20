import logging
import os
import logging
from urllib.parse import quote
from fastapi import FastAPI, Request
from colorama import Fore, Style
from aiogram.exceptions import TelegramForbiddenError
from au_b24 import get_lead, get_user
from e5lib.funcs import phone_purge
from aulib.au_engine import get_engines
from _bot import bot
from ._storage import get_chat_id, set_stage_hash

fastapi_app = FastAPI()

@fastapi_app.post("/lead")
async def process_distributed_lead(request: Request):
    form = await request.form()
    if not form:
        return
    value = form.get("document_id[2]")
    if not value or not isinstance(value, str):
        return
    lead_id = value.split("_")[1]
    chat_id = get_chat_id(lead_id)
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
        await bot.send_message(chat_id, os.getenv("LEAD_DIST_TEXT").format(user.get("NAME"), wa_link))
        logging.info(f"{Fore.LIGHTGREEN_EX}Sent dist text to {lead_id}{Style.RESET_ALL}")
    except TelegramForbiddenError as e:
        logging.error(f"{Fore.RED}TelegramForbiddenError: {e}{Style.RESET_ALL}")
    set_stage_hash(chat_id, "-1")
    return
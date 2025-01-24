import logging
import os
import logging
import requests
from requests.exceptions import RequestException
from pyotp import TOTP
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

totp = TOTP(os.getenv("TOTP_SECRET_KEY"))

def _get_telegram_link(user_id: str | int) -> str | None:
    headers = {"Authorization": totp.now()}
    json = {"user_id": user_id}
    try:
        with requests.Session() as session:
            response = session.post(os.getenv("TELEGRAM_CHANNELS_CREDEINTIALS_ENDPOINT"), json=json, headers=headers, timeout=10)
            if not response.status_code == 200:
                return
            channels = response.json().get("channels")
            if not channels:
                return
            username = channels[0].get("username")
            if username:            
                return f"https://t.me/{username}"
            else:
                phone = channels[0].get("phone")
                return f"https://t.me/+{phone}"
    except RequestException as e:
        logging.error(f"{Fore.RED}RequestException: failed to get telegram channels for user_id {user_id}: {e}{Style.RESET_ALL}")

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
    base_text = os.getenv("LEAD_DIST_TEXT").format(user.get("NAME"))
    links_text = None
    engines = get_engines(user_id)
    if engines:
        wa_link = os.getenv("WA_API_URL").format(phone=phone_purge(engines[0].wid), text=quote(os.getenv("WA_FIRST_MESSAGE_TEXT")))
        links_text = "\n\nWhatsApp:\n" + wa_link
    telegram_link = _get_telegram_link(user_id)
    if telegram_link:
        links_text += "\n\nTelegram:\n" + telegram_link
    if links_text:
        text = base_text + "\n\nНапишите нам напрямую:" + links_text
    else:
        text = base_text + "\n\nПожалуйста, подождите, пока с вами свяжутся"
    try:
        await bot.send_message(chat_id, text)
        logging.info(f"{Fore.LIGHTGREEN_EX}Sent dist text to {lead_id}{Style.RESET_ALL}")
    except TelegramForbiddenError as e:
        logging.error(f"{Fore.RED}TelegramForbiddenError: {e}{Style.RESET_ALL}")
    set_stage_hash(chat_id, "-1")
    return
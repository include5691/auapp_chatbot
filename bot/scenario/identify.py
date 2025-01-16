import logging
import os
import logging
from colorama import Fore, Style
from aiogram.types import Message
from au_b24 import get_leads, update_lead
from e5lib.funcs import phone_purge, create_phone_vars
from e5lib.time import get_yesterday
from ..types import Lead
from .._storage import set_lead

async def identify_user(message: Message) -> None:
    "User identification with phone"
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
        leads = get_leads(filters={"PHONE": phone, ">DATE_CREATE": get_yesterday()}, select=["ID", "NAME", "UF_CRM_MAKE", "UF_CRM_MODEL", "UF_CRM_YEAR"], order="DESC")
        if leads:
            lead = leads[0]
            break
    if not lead:
        logging.info(f"{Fore.RED}Lead not found{Style.RESET_ALL}")
        await message.answer(os.getenv("LEAD_NOT_FOUND_TEXT"))
        return
    lead_id = lead.get("ID")
    set_lead(Lead(**lead), message.chat.id)
    await message.answer(os.getenv("LEAD_FOUND_TEXT").format(lead_id))
    if message.from_user and message.from_user.username:
        update_lead(lead_id, {os.getenv("TELEGRAM_LINK_FIELD_ID"): f"https://t.me/{message.from_user.username}"})
        logging.info(f"{Fore.GREEN}Updated lead {lead_id} with tg username {message.from_user.username}{Style.RESET_ALL}")
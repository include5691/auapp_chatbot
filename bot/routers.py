import logging
import os
import logging
from colorama import Fore, Style
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from au_b24 import get_leads, update_lead
from e5lib.time import get_yesterday
from e5lib.funcs import phone_purge, create_phone_vars
from .types import Lead
from ._scenario import get_next_node
from ._storage import get_stage_hash, reset_stage_hash, set_lead

router = Router()

async def _identify_user(message: Message) -> True | None:
    "User identification with phone"
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
    for phone_var in phone_vars:
        leads = get_leads(filters={"PHONE": phone_var, ">DATE_CREATE": get_yesterday()}, select=["ID", "NAME", "UF_CRM_MAKE", "UF_CRM_MODEL", "UF_CRM_YEAR"], order="DESC")
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
    if message.from_user:
        if message.from_user.username:
            link = f"https://t.me/{message.from_user.username}"
        else:
            link = f"https://t.me/+{phone}"
        update_lead(lead_id, {os.getenv("TELEGRAM_LINK_FIELD_ID"): link})
        logging.info(f"{Fore.GREEN}Updated lead {lead_id} with tg username {message.from_user.username}{Style.RESET_ALL}")
        return True

@router.message(CommandStart())
async def begin_handler(message: Message) -> None:
    await message.answer(os.getenv("WELCOME_TEXT"))
    reset_stage_hash(message.chat.id)

@router.message()
async def handle_message(message: Message) -> None:
    logging.info(message.text)
    stage_hash = get_stage_hash(message.chat.id)
    if not stage_hash:
        if not await _identify_user(message):
            return
    node = get_next_node(stage_hash)
    if not node:
        await message.answer(os.getenv("BEATOFF_TEXT"))
        return

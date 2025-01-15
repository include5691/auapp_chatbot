import logging
import os
import logging
from colorama import Fore, Style
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from au_b24 import get_leads, update_lead
from e5lib.funcs import phone_purge, create_phone_vars
from e5lib.time import get_yesterday
from _redis import redis_cli

router = Router()

@router.message(CommandStart())
async def begin_handler(message: Message) -> None:
    await message.answer(os.getenv("WELCOME_TEXT"))

@router.message()
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

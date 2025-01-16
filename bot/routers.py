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
from .scenario import identify_user
from ._storage import get_stage_hash, reset_stage_hash

router = Router()

@router.message(CommandStart())
async def begin_handler(message: Message) -> None:
    await message.answer(os.getenv("WELCOME_TEXT"))
    reset_stage_hash(message.chat.id)

@router.message()
async def handle_message(message: Message) -> None:
    logging.info(message.text)
    stage_hash = get_stage_hash(message.chat.id)
    if not stage_hash:
        await identify_user(message)
    
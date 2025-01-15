import os
from _redis import redis_cli
from .types import Lead

def get_stage_hash(chat_id: str) -> str | None:
    "Get stage hash for scenario"
    value = redis_cli.get(os.getenv("SCENARIO_HASH_KEY").format(chat_id))
    if value:
        return value.decode()
    return None

def reset_stage_hash(client_id: str) -> None:
    "Reset stage hash for scenario"
    redis_cli.delete(os.getenv("SCENARIO_HASH_KEY").format(client_id))

def set_lead(lead: Lead, chat_id: str) -> None:
    "Set lead to storage"
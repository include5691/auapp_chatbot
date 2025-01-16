import os
from _redis import redis_cli
from .types import Lead

def get_stage_hash(chat_id: str) -> str | None:
    "Get stage hash for scenario"
    value = redis_cli.get(os.getenv("SCENARIO_HASH_KEY").format(chat_id=chat_id))
    if value:
        return value.decode()
    return None

def set_stage_hash(chat_id: str, value: str) -> None:
    "Set stage hash for scenario"
    redis_cli.set(os.getenv("SCENARIO_HASH_KEY").format(chat_id=chat_id), value, ex=7*86400)

def reset_stage_hash(chat_id: str) -> None:
    "Reset stage hash for scenario"
    redis_cli.delete(os.getenv("SCENARIO_HASH_KEY").format(chat_id=chat_id))

def set_lead(lead: Lead, chat_id: str) -> None:
    "Set lead to storage"
    redis_cli.set(os.getenv("CHAT_ID_KEY").format(lead_id=lead.id), chat_id, ex=7*86400)
    redis_cli.hset(os.getenv("LEAD_DATA_KEY").format(chat_id=chat_id), mapping=lead.model_dump())

def get_lead(chat_id: str) -> Lead | None:
    "Get lead from storage"
    data = redis_cli.hgetall(os.getenv("LEAD_DATA_KEY").format(chat_id=chat_id))
    if data:
        return Lead(**{k.decode(): v.decode() for k, v in data.items()})
    return None

def get_chat_id(lead_id: str) -> str | None:
    "Get chat id from storage"
    value = redis_cli.get(os.getenv("CHAT_ID_KEY").format(lead_id=lead_id))
    if value:
        return value.decode()
    return None
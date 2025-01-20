import os
from au_sheets import get_df
from .types import Node

def get_next_node(stage_hash: str | None = None) -> Node | None:
    "Get next node from scenario table based on chat_id stage hash"
    df = get_df(os.getenv("CHATBOT_SCENARIO_SHEET"), "сценарий")
    if df is None or df.empty:
        return None
    column = df.iloc[:, 0]
    if not stage_hash:
        return Node(text=column[0])
    previous_node = None
    for value in column:
        node = Node(text=value)
        if previous_node:
            if previous_node.stage_hash == stage_hash:
                return node
        previous_node = node
    return None
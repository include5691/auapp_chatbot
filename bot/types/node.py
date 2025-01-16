import hashlib
from pydantic import BaseModel, model_validator

class Node(BaseModel):
    """Scenario Node for chatbot"""

    text: str # text of the node 
    stage_hash: str # current hash of the node in sha224 format

    @model_validator(mode="before")
    @classmethod
    def validate_node(cls, data: dict) -> dict:
        """Validate the node"""
        data["stage_hash"] = data.get("stage_hash") or hashlib.sha224(data["text"].encode()).hexdigest()
        return data
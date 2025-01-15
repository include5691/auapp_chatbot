from pydantic import BaseModel, model_validator
from e5nlp import filter_name, Car

class Lead(BaseModel):
    "Storage lead presentation"

    lead_id: str
    car_name: str | None = None
    customer_name: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_lead(cls, data: dict) -> dict:
        car_name = Car(**data).get_car_name()
        if car_name:
            data["car_name"] = car_name
        customer_name = filter_name(data.get("NAME", ""))
        if customer_name:
            data["customer_name"] = customer_name
        return data
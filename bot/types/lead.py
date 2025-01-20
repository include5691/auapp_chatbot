from pydantic import BaseModel, model_validator, model_serializer
from e5nlp import filter_name, Car

class Lead(BaseModel):
    "Storage lead presentation"

    id: str
    car_name: str | None = None
    customer_name: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_lead(cls, data: dict) -> dict:
        data["id"] = data.get("id") or data.get("ID") or data.get("lead_id")
        car_name = Car(**data).get_car_name()
        if car_name:
            data["car_name"] = car_name
        customer_name = filter_name(data.get("NAME", ""))
        if customer_name:
            data["customer_name"] = customer_name
        return data

    @model_serializer
    def serialize(self):
        return {k: v for k in vars(self) if (v := getattr(self, k)) is not None}
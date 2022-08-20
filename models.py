from pydantic import BaseModel


class Id(BaseModel):
    id: int


class Customer(BaseModel):
    email: str
    phone: str
    name: str
    bid_type: int

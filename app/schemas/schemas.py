import datetime
from typing import Optional

from pydantic import BaseModel, conint, constr


class ClientSchema(BaseModel):
    name: constr(max_length=50, min_length=1, strict=True)
    surname: constr(max_length=50, min_length=1, strict=True)
    credit_card: Optional[constr(max_length=50)]
    car_number: Optional[constr(max_length=10)]

    class Config:
        orm_mode = True


class ResponseClientSchema(ClientSchema):
    id: int


class ParkingSchema(BaseModel):
    address: constr(max_length=50, min_length=1, strict=True)
    opened: bool
    count_places: int
    count_available_places: int

    class Config:
        orm_mode = True


class ClientParkingSchema(BaseModel):
    client_id: int
    parking_id: int
    time_in: datetime.datetime
    time_out: datetime.datetime

    class Config:
        orm_mode = True


class ClientParkingParametersSchema(BaseModel):
    client_id: conint(strict=True)
    parking_id: conint(strict=True)

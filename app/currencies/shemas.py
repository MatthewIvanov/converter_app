from decimal import Decimal

from pydantic import BaseModel, Field, condecimal


class SCurrencies(BaseModel):
    cur_abbreviation: str = Field(..., example="AUD", max_length=10)
    cur_scale: int = Field(..., example=1, gt=0)
    cur_name: str = Field(..., example="Австралийский доллар", max_length=100)
    cur_officialrate: Decimal = Field(ge=0.0001, decimal_places=4)


class CurrencyResponse(SCurrencies):
    id: int

    class Config:
        from_attributes = True
        json_encoders = {Decimal: lambda v: float(v)}

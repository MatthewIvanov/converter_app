from datetime import date, datetime
from decimal import Decimal
from typing import Literal, Optional

from fastapi import Query
from pydantic import BaseModel, Field, constr
from sqlalchemy import Enum

VALID_CURRENCIES = Literal[
    "AUD",
    "AMD",
    "BGN",
    "BRL",
    "UAH",
    "DKK",
    "AED",
    "USD",
    "VND",
    "EUR",
    "PLN",
    "JPY",
    "INR",
    "IRR",
    "ISK",
    "CAD",
    "CNY",
    "KWD",
    "MDL",
    "NZD",
    "NOK",
    "RUB",
    "XDR",
    "SGD",
    "KGS",
    "KZT",
    "TRY",
    "GBP",
    "CZK",
    "SEK",
    "CHF",
    "BYN",
]


class SExchanges(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Сумма должна быть больше 1")
    from_currency: VALID_CURRENCIES
    to_currency: VALID_CURRENCIES


class ExchangesBase(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Сумма для обмена")
    from_currency: str = Field(..., min_length=3, description="Исходная валюта")
    to_currency: str = Field(..., min_length=3, description="Целевая валюта ")
    exchange_rate: Decimal = Field(..., description="Курс обмена")
    converted_amount: Decimal = Field(..., description="Cумма в целевой валюте")
    status: Literal["pending", "completed", "cancelled"] = Field(
        default="pending", description="Статус сделки"
    )


class ExchangeRequest(BaseModel):
    date_from: date = Query(default=date.today())
    date_to: date = Query(default=date.today())
    currency: Optional[VALID_CURRENCIES] = Query(default=None)  # type: ignore


class ExchangesStatusUpdate(BaseModel):
    exchange_id: int
    result: Literal["Конвертировать", "Отменить"]

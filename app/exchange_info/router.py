from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import case, func, select

from app.currencies.dao import CurrenciesDAO
from app.exchange_info.dao import ExchangesDAO
from app.exchange_info.models import Exchanges
from app.exchange_info.shemas import ExchangeRequest, ExchangesStatusUpdate, SExchanges

router = APIRouter(prefix="/api/exchange", tags=["Конвертация"])


@router.get("/in-pending")
async def get_pending():
    """Предоставляет список незавершенных сделок"""
    result = await ExchangesDAO.find_all_pending()
    return result


@router.get("/offer-list")
async def get_filtered_data(data: ExchangeRequest = Depends()):
    """Предоставляет информацию о сделках за интервал времени. На вход: дата с, дата по, валюта(опционально)"""
    date_from = datetime.combine(data.date_from, datetime.min.time())
    date_to = datetime.combine(data.date_to, datetime.max.time())
    if data.currency:
        result = await ExchangesDAO.find_one_currency(date_from, date_to, data.currency)

        if not result:
            raise HTTPException(status_code=404, detail="Нету данных об сделке")

        total_from, total_to, total_exchange = result.fetchone()
        return {
            "Currency": data.currency,
            "Sum_in": total_from,
            "Sum_out": total_to,
            "Count_exchanges": total_exchange,
        }
    else:
        result = await ExchangesDAO.find_all_currency(date_from, date_to)
        result = result.fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="Нету данных об сделках")

        return [
            {
                "Currency": currency,
                "Sum_in": total_from,
                "Sum_out": total_to,
                "Count_exchanges": total_exchange,
            }
            for currency, total_from, total_to, total_exchange in result
        ]


@router.post("/confirmation")
async def process_exchange(data: ExchangesStatusUpdate):
    """Подтверждение/отмена сделки. На вход индентификатор(id) сделки, конвертировать/отменить. На выход индентификатор(id) сделки, статус сделки"""

    exchange = await ExchangesDAO.find_by_id(data.exchange_id)
    if not exchange:
        raise HTTPException(status_code=404, detail="Сделка не найдена")

    if exchange.status != "pending":
        raise HTTPException(status_code=400, detail="Сделка уже обработана")

    status = {"Конвертировать": "completed", "Отменить": "cancelled"}
    new_status = status.get(data.result)

    if not new_status:
        raise HTTPException(
            status_code=400,
            detail="Неверная строка. Допустимые значения: 'Конвертировать' или 'Отменить'",
        )

    exchange = await ExchangesDAO.update_status(data.exchange_id, new_status)

    return {"exchange_id": exchange.id, "new_status": exchange.status}


@router.post("/offer-info")
async def get_exchange_info(data: SExchanges):
    """Предоставляет информацию о совершаемом обмене. На вход количество валюты на вход, аббревиатура исходной валюты, аббревиатура получаемой валюты. Список доступных валют можно посмотреть в ручке. GET/api/get_rates"""

    if data.to_currency == data.from_currency:
        return {
            "message": f"Вы пытаетесь перевести {data.to_currency} в {data.from_currency}"
        }

    elif data.to_currency == "BYN":
        from_currency = await CurrenciesDAO.find_by_abbreviation(data.from_currency)
        exchange_rate = Decimal(from_currency.Cur_OfficialRate) / Decimal(
            from_currency.Cur_Scale
        )
        converted_amount = data.amount * exchange_rate
        target_currency = "BYN"
        original_currency = from_currency.Cur_Abbreviation

    elif data.from_currency == "BYN":
        to_currency = await CurrenciesDAO.find_by_abbreviation(data.to_currency)
        exchange_rate = Decimal(1) / (
            Decimal(to_currency.Cur_OfficialRate) / Decimal(to_currency.Cur_Scale)
        )
        converted_amount = data.amount * exchange_rate
        target_currency = to_currency.Cur_Abbreviation
        original_currency = "BYN"
    else:
        from_currency = await CurrenciesDAO.find_by_abbreviation(data.from_currency)
        to_currency = await CurrenciesDAO.find_by_abbreviation(data.to_currency)

        # S2 = S1 * (R1 / R2) * (Q2 / Q1).
        exchange_rate = (
            Decimal(from_currency.Cur_OfficialRate)
            / Decimal(to_currency.Cur_OfficialRate)
        ) * (Decimal(to_currency.Cur_Scale) / Decimal(from_currency.Cur_Scale))
        converted_amount = data.amount * exchange_rate
        target_currency = to_currency.Cur_Abbreviation
        original_currency = from_currency.Cur_Abbreviation

    add_exchange = await ExchangesDAO.add(
        data.amount,
        original_currency,
        target_currency,
        exchange_rate,
        converted_amount,
        "pending",
        datetime.now(),
    )

    return {
        "Amount-in-target-currency": add_exchange.converted_amount,
        "Rate": add_exchange.exchange_rate,
        "Id": add_exchange.id,
    }

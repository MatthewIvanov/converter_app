from datetime import date
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import case, func, insert, select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exchange_info.models import Exchanges


class ExchangesDAO(BaseDAO):
    model = Exchanges

    @classmethod
    async def find_one_currency(cls, date_from, date_to, currency):
        async with async_session_maker() as session:
            query = select(
                func.coalesce(
                    func.sum(
                        case((Exchanges.from_currency == currency, Exchanges.amount))
                    ),
                    0,
                ).label("total_from"),
                func.coalesce(
                    func.sum(
                        case(
                            (
                                Exchanges.to_currency == currency,
                                Exchanges.converted_amount,
                            )
                        )
                    ),
                    0,
                ).label("total_to"),
                func.count().label("total_exchange"),
            ).where(
                Exchanges.created_at.between(date_from, date_to),
                Exchanges.status == "completed",
            )
            result = await session.execute(query)
            return result

    @classmethod
    async def find_all_currency(cls, date_from, date_to):
        async with async_session_maker() as session:
            query = (
                select(
                    Exchanges.from_currency.label("currency"),
                    func.coalesce(func.sum(Exchanges.amount), 0).label("total_from"),
                    func.coalesce(func.sum(Exchanges.converted_amount), 0).label(
                        "total_to"
                    ),
                    func.count().label("total_exchange"),
                )
                .where(
                    Exchanges.created_at.between(date_from, date_to),
                    Exchanges.status == "completed",
                )
                .group_by(Exchanges.from_currency)
            )

            result = await session.execute(query)
            return result

    @classmethod
    async def find_all_pending(cls):
        async with async_session_maker() as session:
            query = select(Exchanges).where(Exchanges.status == "pending")
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def update_status(cls, exchange_id: int, new_status: str):
        async with async_session_maker() as session:
            exchange = await session.get(cls.model, exchange_id)
            exchange.status = new_status
            await session.commit()
            await session.refresh(exchange)
            return exchange

    @classmethod
    async def find_by_id(cls, exchange_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == exchange_id)
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def add(
        cls,
        amount: Decimal,
        from_currency: str,
        to_currency: str,
        exchange_rate: Decimal,
        converted_amount: Decimal,
        status: str,
        created_at: date,
    ):

        async with async_session_maker() as session:
            add_exchange = (
                insert(Exchanges)
                .values(
                    amount=amount,
                    from_currency=from_currency,
                    to_currency=to_currency,
                    exchange_rate=exchange_rate,
                    converted_amount=converted_amount,
                    status=status,
                    created_at=created_at,
                )
                .returning(Exchanges)
            )
            new_exchange = await session.execute(add_exchange)
            await session.commit()
            new_exchange = new_exchange.scalar_one()
            return new_exchange

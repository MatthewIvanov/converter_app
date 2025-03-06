from sqlalchemy import delete, insert, select

from app.currencies.models import Currencies
from app.dao.base import BaseDAO
from app.database import async_session_maker


class CurrenciesDAO(BaseDAO):
    model = Currencies

    @classmethod
    async def add_rates(cls, data):
        async with async_session_maker() as session:
            add_currencies = insert(cls.model).values(data)
            await session.execute(add_currencies)
            await session.commit()
        return data

    @classmethod
    async def find_by_abbreviation(cls, abbreviation: str):
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.Cur_Abbreviation == abbreviation)
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def delete_all(cls):
        async with async_session_maker() as session:
            await session.execute(delete(cls.model))
            await session.commit()

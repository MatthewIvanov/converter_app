from contextlib import asynccontextmanager
from datetime import date, datetime
from decimal import Decimal
import time
from typing import Annotated

import httpx
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI, HTTPException, Query, Request
from sqlalchemy import Date, cast, select
from fastapi.middleware.cors import CORSMiddleware

from app.currencies.dao import CurrenciesDAO
from app.currencies.models import Currencies
from app.database import async_session_maker
from app.exchange_info.router import router as router_exchange_info

from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Обращение к API ежедневно в 00:00:00"""
    scheduler = AsyncIOScheduler(timezone="Europe/Minsk")
    trigger = CronTrigger(
        hour=0,
        minute=0,
        timezone=pytz.timezone("Europe/Minsk")
    )
    
    scheduler.add_job(my_scheduled_function, trigger)
    scheduler.start()
    
    yield
    scheduler.shutdown(wait=False)

app = FastAPI(lifespan=lifespan)
app.include_router(router_exchange_info)

async def get_api_rates():
    """Сбор курсов валют с API"""
    async with async_session_maker() as session:
        currencies = await session.execute(
            select(Currencies).where(cast(Currencies.Date, Date) == date.today())
        )
        
        async with httpx.AsyncClient() as client:  
            response = await client.get("https://api.nbrb.by/exrates/rates?periodicity=0")
            
            if response.status_code != 200:
                print("Ошибка при получении данных с API")
                return
            
            data = response.json()
            
            if currencies.scalars().first():
                print("Курсы уже добавлены")
            else:
                for item in data:
                    item["Date"] = datetime.strptime(item["Date"], "%Y-%m-%dT%H:%M:%S")
                await CurrenciesDAO.add_rates(data)
            return data

async def my_scheduled_function():
    await CurrenciesDAO.delete_all()
    await get_api_rates()
    print("Новые курсы добавлены")

@app.get("/api/get_rates")
async def get_rates():
    """Получить все курсы валют"""
    return await get_api_rates()






origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Coontent-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Authorization",
    ],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        "Request handling time ", extra={"process_time": round(process_time, 4)}
    )
    return response
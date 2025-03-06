from sqlalchemy import JSON, Column, DateTime, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Currencies(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True)
    Cur_ID = Column(Integer, nullable=False)
    Date = Column(DateTime, nullable=False)
    Cur_Abbreviation = Column(String, nullable=False)
    Cur_Scale = Column(Integer, nullable=False)
    Cur_Name = Column(String, nullable=False)
    Cur_OfficialRate = Column(Numeric(10, 4), nullable=False)

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Exchanges(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(12, 4), nullable=False)
    from_currency = Column(String(10), nullable=False)
    to_currency = Column(String(10), nullable=False)
    exchange_rate = Column(Numeric(12, 4), nullable=False)
    converted_amount = Column(Numeric(12, 4), nullable=False)
    status = Column(String(15), default="pending", nullable=False)
    created_at = Column(DateTime, nullable=False)

    __table_args__ = (
        Index("idx_date_status_currency", created_at, status, to_currency),
    )

    def __repr__(self):
        return f"<Exchange(id={self.id}, {self.amount} {self.from_currency} → {self.converted_amount} {self.to_currency} @ {self.exchange_rate}, status={self.status})>"

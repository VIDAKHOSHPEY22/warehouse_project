"""
models/location.py
----------------------------------------------------------------
مکان فیزیکی نگهداری کالا داخل انبار (Bin/Rack/Zone).
مدل‌سازی جداگانه Location به ما اجازه می‌دهد بدانیم هر بچ از هر
کالا دقیقا کجای انبار قرار دارد (لازم برای Put-away و Picking).
----------------------------------------------------------------
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)  # مثلا A1-R2-B3
    name: Mapped[str] = mapped_column(String(128), nullable=False)  # مثلا "قفسه غذایی - ردیف ۲"
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    batches = relationship("Batch", back_populates="location")

"""
models/mission.py
----------------------------------------------------------------
مأموریت/درخواست توزیع (Mission/Request).
نماینده‌ی یک نیاز مشخص است (مثلا "توزیع کمک به روستای X") که
اقلام از انبار به آن تخصیص داده و در نهایت تحویل داده می‌شوند.
----------------------------------------------------------------
"""
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import MissionStatus


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    requester: Mapped[str | None] = mapped_column(String(128), nullable=True)  # درخواست‌کننده/نهاد
    destination: Mapped[str | None] = mapped_column(String(128), nullable=True)  # مقصد جغرافیایی
    status: Mapped[MissionStatus] = mapped_column(SAEnum(MissionStatus), default=MissionStatus.DRAFT)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)

    transactions = relationship("Transaction", back_populates="mission")

from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Setting(Base):
    __tablename__ = "settings"
    id: Mapped[int] = mapped_column(primary_key=True)
    start: Mapped[str] = mapped_column(Text(), nullable=True)
    tech: Mapped[str] = mapped_column(Text(), nullable=True)
    exchange: Mapped[str] = mapped_column(Text(), nullable=True)
    start_photo: Mapped[str] = mapped_column(String(), nullable=True)
    tech_photo: Mapped[str] = mapped_column(String(), nullable=True)
    exchange_photo: Mapped[str] = mapped_column(String(), nullable=True)

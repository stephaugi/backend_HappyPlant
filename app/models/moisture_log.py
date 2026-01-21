from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import datetime
from ..db import db

class MoistureLog(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time_stamp: Mapped[datetime]
    moisture_level: Mapped[int]
    plant_id: Mapped[list[int]] = mapped_column(ForeignKey("plant.id"))
    plant: Mapped[Optional["Plant"]] = relationship(back_populates="moisture_history")

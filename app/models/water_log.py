from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import datetime
from ..db import db

class WaterLog(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time_stamp: Mapped[datetime]
    plant_id: Mapped[Optional[int]] = mapped_column(ForeignKey("plant.id"))
    plant: Mapped[Optional["Plant"]] = relationship(back_populates="water_history")

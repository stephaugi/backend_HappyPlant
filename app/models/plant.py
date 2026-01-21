from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import datetime
from ..db import db

class Plant(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    photo: Mapped[Optional[str]] = mapped_column(default=None)
    current_moisture_level: Mapped[Optional[int]] 
    desired_moisture_level: Mapped[int]
    next_water_date: Mapped[Optional[datetime]] = mapped_column(default=None)
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("owner.id"))
    owner: Mapped[Optional["Owner"]] = relationship(back_populates="plants")
    water_history: Mapped[list["WaterLog"]] = relationship(back_populates="plant")
    moisture_history: Mapped[list["MoistureLog"]] = relationship(back_populates="plant")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id
        }
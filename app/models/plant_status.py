from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import date
from ..db import db

class PlantStatus(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time_stamp: Mapped[date]
    moisture_level: Mapped[int]
    water: Mapped[bool]
    plant_id: Mapped[list[int]] = mapped_column(ForeignKey("plant.id"))
    plant: Mapped[Optional["Plant"]] = relationship(back_populates="plant_status")

    def to_dict(self):
        return {
            "id": self.id,
            "time_stamp": str(self.time_stamp),
            "moisture_level": self.moisture_level,
            "water": self.water,
            "plant_id": self.plant_id,
            "plant": self.plant.name
        }

    @classmethod
    def from_dict(cls, data):
        required_params = ["time_stamp", "plant_id", "moisture_level", "water"]
        kwarg_dict = {param: data[param] for param in required_params}
        return cls(**kwarg_dict)
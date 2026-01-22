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

    def to_dict(self):
        return {
            "id": self.id,
            "time_stamp": self.name,
            "plant_id": self.plant_id,
            "plant": self.plant.name
        }

    @classmethod
    def from_dict(cls, data):
        required_params = ["time_stamp", "plant_id"]
        kwarg_dict = {param: data[param] for param in required_params}
        return cls(**kwarg_dict)
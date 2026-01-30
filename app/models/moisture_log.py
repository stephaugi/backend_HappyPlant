from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from datetime import date
from ..db import db

class MoistureLog(db.Model):
    __table_name__: "moisture_log"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[Optional[date]]
    moisture_level: Mapped[Optional[int]]
    plant_id: Mapped[Optional[list[int]]] = mapped_column(ForeignKey("plant.id"))
    plant: Mapped[Optional["Plant"]] = relationship(back_populates="moisture_history")

    def to_dict(self):
        
        return {
            "id": self.id,
            "timestamp": str(self.timestamp),
            "moisture_level": self.moisture_level,
        }

    @classmethod
    def from_dict(cls, data):
        required_params = ["timestamp", "plant_id", "moisture_level"]
        kwarg_dict = {param: data[param] for param in required_params}
        return cls(**kwarg_dict)
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import ForeignKey
from typing import Optional
# from datetime import datetime
from ..db import db

class Owner(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    plants: Mapped[list["Plant"]] = relationship(back_populates="owner")

    def to_dict(self, plant_list=False):
        response_dict = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
        all_plants= []
        if self.plants:
            all_plants = [plant.to_dict() for plant in self.plants]
        
        response_dict["plants"]= all_plants

        return response_dict
    
    @classmethod
    def from_dict(cls, owner_data):
        params = ["id", "first_name", "last_name", "email", "plants"]
        kwarg_dict = {param: owner_data[param] for param in params}

        return cls(**kwarg_dict)
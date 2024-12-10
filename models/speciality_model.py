from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey

from sqlalchemy.orm import relationship

from database.db import db

class Speciality(db.Model):
  id = Column(Integer, primary_key=True)
  speciality = Column(String(50), nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.now())

  doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
  doctor = relationship("Doctor", back_populates="speciality")

  def __repr__(self) -> str:
    return f'Speciality({self.id}, {self.speciality}, {self.created_at})'
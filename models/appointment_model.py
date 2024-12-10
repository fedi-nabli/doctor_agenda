from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum as SqlEnum

from database.db import db

class AppointmentStatusEnum(Enum):
  PENDING = 'PENDING'
  ACCEPTED = 'ACCEPTED'
  REFUSED = 'REFUSED'

class Appointment(db.Model):
  id = Column(Integer, primary_key=True)
  doctor = Column(Integer, ForeignKey('doctor.id'), nullable=False)
  patient = Column(Integer, ForeignKey('patient.id'), nullable=False)
  date = Column(DateTime, nullable=False)
  status = Column(SqlEnum(AppointmentStatusEnum), nullable=False, default=AppointmentStatusEnum.PENDING)
  created_at = Column(DateTime, nullable=False, default=datetime.now())

  def __repr__(self) -> str:
    return f'Appointment({self.id}, {self.date}, {self.status})'
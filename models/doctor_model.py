from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database.db import db

class Address(db.Model):
  id = Column(Integer, primary_key=True)
  ville = Column(String(150), nullable=False)
  gouvernerat = Column(String(150), nullable=False)
  postal_code = Column(String(5), nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.now())

  doctor = relationship("Doctor", back_populates="address", uselist=False)

  def __repr__(self) -> str:
    return f'Address({self.id}, {self.ville}, {self.gouvernerat}, {self.postal_code})'

class Doctor(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(40), nullable=False)
  prenom = Column(String(40), nullable=False)
  email = Column(String(255), nullable=False, unique=True)
  password = Column(String(255), nullable=False)
  phone = Column(String(8), nullable=False)
  max_rendez_vous = Column(Integer, nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.now())

  address_id = Column(Integer, ForeignKey('address.id'), unique=True, nullable=False)
  address = relationship("Address", back_populates="doctor", uselist=False)

  speciality = relationship("Speciality", back_populates="doctor", uselist=True)

  def __repr__(self) -> str:
    return f'Doctor({self.email}, {self.id}, {self.name}, {self.prenom})'
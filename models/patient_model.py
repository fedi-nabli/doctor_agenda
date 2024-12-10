from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer

from database.db import db

class Patient(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(40), nullable=False)
  prenom = Column(String(40), nullable=False)
  email = Column(String(255), nullable=False, unique=True)
  password = Column(String(255), nullable=False)
  phone = Column(String(8), nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.now())

  def __repr__(self):
    return f'Patient({self.email}, {self.id}, {self.name}, {self.prenom})'
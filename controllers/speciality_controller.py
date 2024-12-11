from database.db import db
from models.speciality_model import Speciality

def list_specialities(doctor_id: int = None) -> list[dict]:
  speciality_query = Speciality.query

  if doctor_id:
    speciality_query = speciality_query.filter(Speciality.doctor_id == doctor_id)
  
  db_specialities = speciality_query.all()
  return [{
    'id': speciality.id,
    'speciality': speciality.speciality,
    'created_at': speciality.created_at
  } for speciality in db_specialities]

def add_speciality(doctor_id: int, speciality: str) -> dict | None:
  if not doctor_id or not speciality:
    return None
  
  new_speciality = Speciality(doctor_id=doctor_id, speciality=speciality)
  db.session.add(new_speciality)
  db.session.commit()

  return {
    'id': new_speciality.id,
    'speciality': new_speciality.speciality,
    'created_at': new_speciality.created_at
  }

def delete_speciality(speciality_id: int) -> dict | None:
  if not speciality_id:
    return None
  
  speciality = Speciality.query.get(speciality_id)
  if speciality:
    db.session.delete(speciality)
    db.session.commit()
    return {
      'id': speciality.id,
      'speciality': speciality.speciality,
      'created_at': speciality.created_at
    }
  else:
    return None

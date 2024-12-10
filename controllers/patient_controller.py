from database.db import db
from models.patient_model import Patient

def get_patients() -> list[dict] | None:
  db_patients: list[Patient] = Patient.query.all()

  if db_patients:
    patients = [{
      'id': patient.id,
      'name': patient.name,
      'prenom': patient.prenom,
      'email': patient.email,
      'phone': patient.phone,
      'created_at': patient.created_at
    } for patient in db_patients]

    return patients
  else:
    return None
  
def create_patient(patient_data = None) -> dict:
  if not patient_data:
    return None
  
  name = patient_data.get('name')
  prenom = patient_data.get('prenom')
  email = patient_data.get('email')
  password = patient_data.get('password')
  phone = patient_data.get('phone')

  created_patient = Patient(
    name=name,
    prenom=prenom,
    email=email,
    password=password,
    phone=phone
  )

  db.session.add(created_patient)
  db.session.commit()

  patient = {
    'id': created_patient.id,
    'name': created_patient.name,
    'prenom': created_patient.prenom,
    'email': created_patient.email,
    'phone': created_patient.phone,
    'created_at': created_patient.created_at
  }

  return patient

def delete_patient(patient_id: int) -> bool:
  patient = Patient.query.get(patient_id)

  if patient:
    db.session.delete(patient)
    db.session.commit()

    return True
  
  else:
    return False
  
def get_patient_by_id(patient_id: int = None) -> dict | None:
  db_patient = Patient.query.get(patient_id)

  if db_patient:
    patient = {
      'id': db_patient.id,
      'name': db_patient.name,
      'prenom': db_patient.prenom,
      'email': db_patient.email,
      'phone': db_patient.phone,
      'created_at': db_patient.created_at
    }

    return patient
  
  else:
    return None
  
def update_patient(patient_id: int = None, new_data = None) -> dict | None:
  db_patient: Patient = Patient.query.get(patient_id)

  if db_patient:
    if new_data.get('name'):
      db_patient.name = new_data.get('name')

    if new_data.get('prenom'):
      db_patient.prenom = new_data.get('prenom')

    if new_data.get('email'):
      db_patient.email = new_data.get('email')

    if new_data.get('password'):
      db_patient.password = new_data.get('password')

    if new_data.get('phone'):
      db_patient.phone = new_data.get('phone')

    patient = {
      'id': db_patient.id,
      'name': db_patient.name,
      'prenom': db_patient.prenom,
      'email': db_patient.email,
      'phone': db_patient.phone,
      'created_at': db_patient.created_at
    }

    return patient

  else:
    return None
  

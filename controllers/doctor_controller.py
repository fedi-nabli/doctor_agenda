from database.db import db
from models.doctor_model import Doctor, Address

def list_doctors(name: str = None, prenom: str = None, ville: str = None, governerat: str = None) -> list[dict]:
  doctor_query = Doctor.query
  doctor_query = doctor_query.join(Doctor.address)

  if name:
    doctor_query = doctor_query.filter(Doctor.name == name)
  if prenom:
    doctor_query = doctor_query.filter(Doctor.prenom == prenom)
  if ville:
    doctor_query = doctor_query.filter(Address.ville == ville)
  if governerat:
    doctor_query = doctor_query.filter(Address.gouvernerat == governerat)
  
  db_doctors = doctor_query.all()
  return [{
    'id': doctor.id,
    'name': doctor.name,
    'prenom': doctor.prenom,
    'email': doctor.email,
    'phone': doctor.phone, 
    'max_rendez_vous': doctor.max_rendez_vous,
    'address': {
      'ville': doctor.address.ville,
      'gouvernerat': doctor.address.gouvernerat,
      'postal_code': doctor.address.postal_code
    },
    'specialities': [speciality.speciality for speciality in doctor.speciality]
  } for doctor in db_doctors]

def get_doctor_by_id(doctor_id: int = None) -> dict | None:
  if not doctor_id:
    return None
  
  doctor = Doctor.query.get(doctor_id)
  if doctor:
    return {
      'id': doctor.id,
      'name': doctor.name,
      'prenom': doctor.prenom,
      'email': doctor.email,
      'phone': doctor.phone,
      'max_rendez_vous': doctor.max_rendez_vous,
      'address': {
        'ville': doctor.address.ville,
        'gouvernerat': doctor.address.gouvernerat,
        'postal_code': doctor.address.postal_code
      },
      'specialities': [speciality.speciality for speciality in doctor.speciality]
    }
  else:
    return None
  
def create_doctor(doctor_data: dict) -> dict | None:
  if not doctor_data:
    return None
  
  name = doctor_data.get('name')
  prenom = doctor_data.get('prenom')
  email = doctor_data.get('email')
  password = doctor_data.get('password')
  phone = doctor_data.get('phone')
  max_rendez_vous = doctor_data.get('max_rendez_vous')
  ville = doctor_data.get('ville')
  governerat = doctor_data.get('governerat')
  postal_code = doctor_data.get('postal_code')
  
  address = Address(ville=ville, governerat=governerat, postal_code=postal_code)
  db.session.add(address)
  db.session.commit()
  
  created_doctor = Doctor(
    name=name,
    prenom=prenom,
    email=email,
    password=password,
    phone=phone,
    max_rendez_vous=max_rendez_vous,
    address=address
  )
  
  db.session.add(created_doctor)
  db.session.commit()
  
  return {
    'id': created_doctor.id,
    'name': created_doctor.name,
    'prenom': created_doctor.prenom,
    'email': created_doctor.email,
    'phone': created_doctor.phone,
    'max_rendez_vous': created_doctor.max_rendez_vous,
    'address': {
      'ville': created_doctor.address.ville,
      'gouvernerat': created_doctor.address.gouvernerat,
      'postal_code': created_doctor.address.post
    }
  }

def delete_doctor(doctor_id: int) -> bool:
  doctor = Doctor.query.get(doctor_id)
  
  if doctor:
    db.session.delete(doctor)
    db.session.commit()
    
    return True
  else:
    return False
  
def update_doctor(doctor_id: int, doctor_data: dict) -> dict | None:
  if not doctor_data:
    return None
  
  doctor = Doctor.query.get(doctor_id)
  
  if doctor:
    doctor.name = doctor_data.get('name', doctor.name)
    doctor.prenom = doctor_data.get('prenom', doctor.prenom)
    doctor.email = doctor_data.get('email', doctor.email)
    doctor.password = doctor_data.get('password', doctor.password)
    doctor.phone = doctor_data.get('phone', doctor.phone)
    doctor.max_rendez_vous = doctor_data.get('max_rendez_vous', doctor.max_rendez_vous)
    
    address = doctor.address
    address.ville = doctor_data.get('ville', address.ville)
    address.gouvernerat = doctor_data.get('gouvernerat', address.gouvernerat)
    address.postal_code = doctor_data.get('postal_code', address.postal_code)
    
    db.session.commit()
    
    return {
      'id': doctor.id,
      'name': doctor.name,
      'prenom': doctor.prenom,
      'email': doctor.email,
      'phone': doctor.phone,
      'max_rendez_vous': doctor.max_rendez_vous,
      'address': {
        'ville': address.ville,
        'gouvernerat': address.gouvernerat,
        'postal_code': address.postal_code
      },
      'specialities': [speciality.speciality for speciality in doctor.speciality]
    }
  else:
    return None
  
def get_doctor_specialities(doctor_id: int) -> list[dict]:
  doctor: Doctor = Doctor.query.get(doctor_id)
  
  if doctor:
    return [{
      'id': speciality.id,
      'name': speciality.speciality
    } for speciality in doctor.speciality]
  else:
    return None
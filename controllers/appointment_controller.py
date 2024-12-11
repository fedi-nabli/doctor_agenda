from database.db import db
from models.appointment_model import Appointment

from controllers.patient_controller import get_patient_by_id
from controllers.doctor_controller import get_doctor_by_id

def get_appointments() -> list[dict] | None:
  db_appointments: list[Appointment] = Appointment.query.all()

  if db_appointments:
    appointments = [{
      'id': appointment.id,
      'patient': get_patient_by_id(appointment.patient_id),
      'doctor': get_doctor_by_id(appointment.doctor_id),
      'date': appointment.date,
      'status': appointment.status,
      'created_at': appointment.created_at
    } for appointment in db_appointments]

    return appointments
  else:
    return None
  
def get_doctor_appointments(doctor_id: int) -> list[dict] | None:
  db_appointments: list[Appointment] = Appointment.query.filter_by(doctor_id=doctor_id).all()

  if db_appointments:
    appointments = [{
      'id': appointment.id,
      'patient': get_patient_by_id(appointment.patient_id),
      'doctor': get_doctor_by_id(appointment.doctor_id),
      'date': appointment.date,
      'status': appointment.status,
      'created_at': appointment.created_at
    } for appointment in db_appointments]

    return appointments
  else:
    return None
  
def get_patient_appointments(patient_id: int) -> list[dict] | None:
  db_appointments: list[Appointment] = Appointment.query.filter_by(patient_id=patient_id).all()

  if db_appointments:
    appointments = [{
      'id': appointment.id,
      'patient': get_patient_by_id(appointment.patient_id),
      'doctor': get_doctor_by_id(appointment.doctor_id),
      'date': appointment.date,
      'status': appointment.status,
      'created_at': appointment.created_at
    } for appointment in db_appointments]

    return appointments
  else:
    return None

def create_appointment(appointment_data = None) -> dict | str | None:
  if not appointment_data:
    return None
  
  doctor = get_doctor_by_id(appointment_data.get('doctor_id'))
  if not doctor:
    return None
  
  appointments = get_doctor_appointments(doctor.get('id'))

  if appointments:
    counter = 0
    for appointment in appointments:
      if appointment.get('date') == appointment_data.get('date'):
        counter += 1

    if counter >= doctor.get('max_rendez_vous'):
      return 'Exceeded max appointments for this doctor'

  patient_id = appointment_data.get('patient_id')
  doctor_id = appointment_data.get('doctor_id')
  date = appointment_data.get('date')

  created_appointment = Appointment(
    patient_id=patient_id,
    doctor_id=doctor_id,
    date=date
  )

  db.session.add(created_appointment)
  db.session.commit()

  appointment = {
    'id': created_appointment.id,
    'patient': get_patient_by_id(created_appointment.patient_id),
    'doctor': get_doctor_by_id(created_appointment.doctor_id),
    'date': created_appointment.date,
    'status': created_appointment.status,
    'created_at': created_appointment.created_at
  }

  return appointment

def delete_appointment(appointment_id: int) -> bool:
  appointment = Appointment.query.get(appointment_id)

  if appointment:
    db.session.delete(appointment)
    db.session.commit()

    return True
  
  else:
    return False
  
def get_appointment_by_id(appointment_id: int) -> dict | None:
  db_appointment = Appointment.query.get(appointment_id)

  if db_appointment:
    appointment = {
      'id': db_appointment.id,
      'patient': get_patient_by_id(db_appointment.patient_id),
      'doctor': get_doctor_by_id(db_appointment.doctor_id),
      'date': db_appointment.date,
      'status': db_appointment.status,
      'created_at': db_appointment.created_at
    }

    return appointment
  else:
    return None
  
def update_appointment_status(appointment_id: int, status: str) -> dict | None:
  db_appointment = Appointment.query.get(appointment_id)

  if db_appointment:
    db_appointment.status = status
    db.session.commit()

    appointment = {
      'id': db_appointment.id,
      'patient': get_patient_by_id(db_appointment.patient_id),
      'doctor': get_doctor_by_id(db_appointment.doctor_id),
      'date': db_appointment.date,
      'status': db_appointment.status,
      'created_at': db_appointment.created_at
    }

    return appointment
  else:
    return None
  
def cancel_appointment(appointment_id: int) -> bool:
  return update_appointment_status(appointment_id, 'CANCELED') is not None

def accept_appointment(appointment_id: int) -> bool:
  return update_appointment_status(appointment_id, 'ACCEPTED') is not None
import os
import re
from dotenv import load_dotenv
from os.path import join, dirname

from flask import Flask
import mysql.connector as connector
from flask_sqlalchemy import SQLAlchemy

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PASS_ENCODED = os.getenv('DB_PASS_ENCODED')
DB_NAME = os.getenv('DB_NAME')

class DatabaseApi():
  def __init__(self, delete_if_exists: bool = False, app: Flask = None) -> None:
    self.app = app
    connection = connector.connect(
      host=DB_HOST,
      port=DB_PORT,
      user=DB_USER,
      password=DB_PASS
    )

    cursor = connection.cursor()

    cursor.execute('SHOW DATABASES')
    found = False
    for db_name in cursor:
      pattern = "[(,')]"
      db_string = re.sub(pattern, '', str(db_name))
      if db_string == DB_NAME.lower():
        found = True

    if DB_NAME is not None:
      if found == False:
        create_db_query = f"CREATE DATABASE {DB_NAME}"
        cursor.execute(create_db_query)
      elif found:
        if delete_if_exists:
          drop_db_query = f"DROP DATABASE {DB_NAME}"
          cursor.execute(drop_db_query)
          create_db_query = f"CREATE DATABASE {DB_NAME}"
          cursor.execute(create_db_query)

    connection.close()

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASS_ENCODED}@{DB_HOST}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  def create_models(self, db: SQLAlchemy) -> None:
    with self.app.app_context():
      db.create_all()
from flask import Flask
from flask_cors import CORS

from database.db import db
from database.api import DatabaseApi
from utils.error_handler import error_handler

app = Flask(__name__)
CORS(app)
app.config['secret_key'] = 'secret_key'

db_api = DatabaseApi(app=app, delete_if_exists=True)
db.init_app(app)
db_api.create_models(db)

@app.route('/')
def home():
  return 'Hello, World!'

if __name__ == '__main__':
  app.run(debug=True, port=5000)

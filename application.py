import datetime
from flask import Flask, request
from CRUD_m import create_data
from CRUD_m import read_data
from CRUD_m import close_conncection
from CRUD_m import get_connection

app = Flask(__name__)

@app.route("/access_db", methods = ['POST'])
def access_db():
    patient_id = request.json['patient_id']
    device_id = request.json['device_id']
    connection = get_connection()
    date_time = datetime.datetime.now()
    data = {'patient_id':patient_id, 'device_id':device_id, 'medium_count':1, 'time':date_time}
    table_name = 'pedal'
    create_data(table_name, data, connection)
    return str(patient_id)

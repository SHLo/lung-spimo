import datetime
from flask import Flask, request
from CRUD_m import create_data
from CRUD_m import read_data
from CRUD_m import update_data
from CRUD_m import close_connection
from CRUD_m import get_connection
from CRUD_m import read_count

app = Flask(__name__)

@app.route("/paddle_count", methods = ['POST'])
def paddle_count():
    patient_id = request.json['patient_id']
    device_id = request.json['device_id']
    connection = get_connection()
    date_time = datetime.datetime.now()
    data = {'patient_id':patient_id, 'device_id':device_id, 'medium_count':1, 'time':date_time}
    table_name = 'pedal'
    create_data(table_name, data, connection)
    close_connection(connection)
    return str(1)


@app.route("/register_device", methods = ['POST'])
def register_device():
    patient_id = request.json['patient_id']
    spimo_id = request.json['spimo_id']
    pedal_id = request.json['pedal_id']
    date_time = datetime.datetime.now()
    connection = get_connection()
    table_name = 'dp_pair'

    data = {'device_id':spimo_id}
    row = read_data(table_name, data)
    #scenario 2: No such device_id
    if row is None:
        close_connection(connection)
        return str(2)
    #scenario 1: Successful
    elif row.patient_id is None:
        data =  {'patient_id': patient_id, 'updated_date': date_time}
        condition = {'device_id': spimo_id}
        update_data(table_name, data, condition)
        condition = {'device_id': pedal_id}
        update_data(table_name, data, condition)
        close_connection(connection)
        return str(1)
    #scenario 2: duplicated id
    else:
        close_connection(connection)
        return str(0)

@app.route("/return_device", methods = ['POST'])
def return_device():
    patient_id = request.json['patient_id']
    spimo_id = request.json['spimo_id']
    pedal_id = request.json['pedal_id']
    date_time = datetime.datetime.now()
    connection = get_connection()
    table_name = 'dp_pair'
    data = {'device_id':spimo_id}
    row = read_data(table_name, data)
    # device has been returned
    if row.patient_id is None:
        close_connection(connection)
        return str(0)
    else:
        data =  {'patient_id': None, 'updated_date':None}
        condition = {'device_id': spimo_id}
        update_data(table_name, data, condition)
        condition = {'device_id': pedal_id}
        update_data(table_name, data, condition)

        close_connection(connection)
        return str(1)


@app.route('/device_start', methods = ['POST'])
def device_start():
    patient_id = request.json['patient_id']
    device_id = request.json['device_id']
    connection = get_connection()
    date_time = datetime.datetime.now()
    data =  {'start_time': date_time}
    table_name = 'dp_pair'
    condition = {'device_id': device_id, 'patient_id': patient_id}
    update_data(table_name, data, condition)

    close_connection(connection)
    return str(1)


@app.route('/device_refresh', methods = ['GET'])
def device_refresh():
    patient_id = request.args.get('patient_id')
    print(patient_id)
    device_id = request.args.get('device_id')
    print(device_id)
    connection = get_connection()
    table_name = 'dp_pair'
    data = {'device_id':device_id, 'patient_id':patient_id}
    row = read_data(table_name, data)
    start_time = row.start_time
    current_time = datetime.datetime.now()
    if (device_id[0:3] == 'SPI'):
        table_name = 'spimo'
    elif (device_id[0:3] == 'PED'):
        table_name = 'pedal'
    row = read_count(table_name, start_time, current_time, device_id)
    result = row.total_count
    close_connection(connection)
    return str(result)

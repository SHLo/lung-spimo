import datetime
from CRUD_win import create_data
from CRUD_win import read_data
from CRUD_win import update_data
from CRUD_win import read_count
from CRUD_win import get_connection
from CRUD_win import close_connection

if __name__ == '__main__':
    currentDT = datetime.datetime.now()

    # # create_data
    # device_id = 'SPI001'
    # data = {'device_id':device_id}
    # table_name = 'dp_pair'
    # result = read_data(table_name, data)
    # print(result)

    # # #read_data
    # table_name = 'packop_transaction'
    # data = {'date': '2019-02-17','device_id':'123'}
    # read_data(table_name, data)
    #
    # #
    # #update_data
    # table_name = 'dp_pair'
    # data =  {'patient_id': None}
    # condition_id = {'device_id': 'SPI001'}
    # update_data(table_name, data, condition_id)

    # start
    # device_id = 'SPI001'
    # patient_id = 'PAT001'
    # connection = get_connection()
    # date_time = datetime.datetime.now()
    # data =  {'start_time': date_time}
    # condition = {'device_id': device_id, 'patient_id': patient_id}
    # table_name = 'dp_pair'
    # update_data(table_name, data, condition)
    # close_connection(connection)
    # read_count
    device_id = 'SPI002'
    patient_id = 'PAT002'
    table_name = 'dp_pair'
    data = {'device_id':device_id, 'patient_id':patient_id}
    row = read_data(table_name, data)
    print (row)
    start_time = row.start_time
    current_time = datetime.datetime.now()
    if (device_id[0:3] == 'SPI'):
        print(device_id[0:3])
        table_name = 'spimo'
    elif (device_id[0:3] == 'PED'):
        table_name = 'pedal'
    row = read_count(table_name, start_time, current_time, device_id)
    result = row.total_count
    print (result)

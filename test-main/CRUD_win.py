# SQL Server Database Connection Properties

import pyodbc



# Return the sql connection
def get_connection():
    server = 'lung.database.windows.net'
    database = 'lung'
    username = 'pi'
    password = 'R@spberry'
    driver= '{ODBC Driver 13 for SQL Server}'
    connection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    return connection


def close_connection(connection):
    # Commit the data


    # Close the connection
    connection.close()
    print('Connection Closed')


def create_data(table_name, data, connection):
    str = ""
    value_list = []
    #print(data)
    for i in range(len(data)):
        tmpstr = "?,"
        str = str + tmpstr
    sql_query = str[:-1]
    sql_query = "Insert Into " + table_name + " Values("+sql_query+")"
    cursor = connection.cursor()

    for key in data:
         value_list.append(data[key])

    cursor.execute(sql_query, value_list)
    connection.commit()
    #print('Data Saved')
    return connection
    # Commit the data



def read_data(table_name, data):
    # Get the sql connection
    connection = get_connection()
    cursor = connection.cursor()

    sql_query = "select * from " + table_name
    if len(data)>0:
        sql_query = sql_query + " where 1=1"
        for key, value in data.items():
            sql_query = f"{sql_query} and {key} = '{value}'"
            #sql_query = sql_query + " and " + key + " = " + "'" +value+ "'"
    # Execute the sql query
    result = cursor.execute(sql_query)
    row = cursor.fetchone()

    return row

def update_data(table_name, data, condition):
    # Get the sql connection
    value_list = []
    connection = get_connection()
    cursor = connection.cursor()

    #sql_query = "Update " + table_name + " Set "
    sql_query = f"Update {table_name} Set "
    # update table set patient_id=null where device_id = xxx
    # cursor.execute("SELECT * FROM sys.tables")
    if len(data)>0:
        for key in data:
            sql_query = sql_query + key + " = ?, "
        sql_query = sql_query[:-2]
        sql_query = sql_query + " where 1=1"
    if len(condition)>0:
        for key in condition:
            sql_query = sql_query + " and " + key+" =?"

    # Execute the update query
    for key in data:
        value_list.append(data[key])
    for key in condition:
        value_list.append(condition[key])

    cursor.execute(sql_query, value_list)
    connection.commit()
    print('Data Updated Successfully')


def read_count(table_name, start_time, date_time):
    # Get the sql connection
    connection = get_connection()
    cursor = connection.cursor()
    start_time = str(start_time)[0:23]
    print(start_time)
    date_time = str(date_time)[0:23]
    print(date_time)
    sql_query = f"select SUM(best_count) as total_count from {table_name} where time between '{start_time}' and '{date_time}'"
    print (sql_query)
    # Execute the sql query
    result = cursor.execute(sql_query)
    row = cursor.fetchone()
    return row

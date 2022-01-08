import os
import psycopg2

connection = None

def createConnection(fileName='../../../database.ini'):
    try:
        print("Connecting to the PostgreSQL db...")
        __loadConnection(fileName)
        curs = connection.cursor()
        curs.execute("SELECT version()")
        print("PostgreSQL version: ")
        print(curs.fetchone())
        curs.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        closeConnection()

def getConnection():
    return connection

def __loadConnection(fileName):
    global connection

    if not os.path.isfile(fileName):
        raise Exception(f"Input file {fileName} doesn't exist.")

    file = open(fileName, 'r')
    lines = file.readlines()

    if len(lines) < 4:
        raise Exception(f"No much lines in file {fileName}")

    host = getValue("host", lines[0], '=')
    database = getValue("database", lines[1], '=')
    user = getValue("user", lines[2], '=')
    password = getValue("password", lines[3], '=')
    port = getValue("port", lines[4], '=')
    schema = getValue("schema", lines[5], '=')

    connection = psycopg2.connect(host=host, port=port, database=database, user=user, password=password, options=f"-c search_path={schema},public")

def closeConnection():
    if not connection == None:
        connection.commit()
        connection.close()
        print("Database connection closed.")

def getValue(keyName, onString, delimiter):
    if not onString.startswith(keyName):
        raise Exception(f"Line readed in file as not attribut needed {keyName}")
    return onString.split('=')[1].rstrip()

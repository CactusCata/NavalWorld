import utils.db.DDBConnectionLoader as DDBConnectionLoader

ONE = 0
ALL = 1

connection = None

def prepareRequest(request, mod):
    global connection
    if connection == None:
        connection = DDBConnectionLoader.getConnection()
    cur = connection.cursor()
    cur.execute(request)
    res = None
    if mod == ONE:
        res = cur.fetchone()
    elif mod == ALL:
        res = cur.fetchall()
    cur.close()
    return res

def getCountryByID(id):
    return prepareRequest(f"""
        SELECT *
        FROM Country
        WHERE Country.country_id='{id}';
        """, ONE)

def getCountryByName(name):
    return prepareRequest(f"""
        SELECT *
        FROM Country
        WHERE Country.country_name='{name}';
        """, ONE)

def getCountriesAffectionByID(countryID):
    return prepareRequest(f"""
        SELECT *
        FROM Country_Affection
        WHERE Country_Affection.country_id_in='{countryID}'
        AND Country_Affection.country_id_out <> '{countryID}';
        """, ALL)

def __makeRequest(request):
    cur = connection.cursor()
    cur.execute(request)
    cur.close()

def updateRequest(request):
    __makeRequest(request)

def prepareDelete(request):
    __makeRequest(request)

def prepareInsert(request):
    __makeRequest(request)

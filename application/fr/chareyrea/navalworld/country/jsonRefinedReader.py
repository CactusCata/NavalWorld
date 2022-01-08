import json
import os
import country.country as country
from country.country import Country

countries = {}

def loadCountries():
    global countries
    countriesFileName = "../../../res/polygon/countries.geojson"

    if not os.path.isfile(countriesFileName):
        print(f"the file {countriesFileName} doesn't exist !")
        exit(-1)

    countriesFile = open(countriesFileName, "r")

    countriesProperties = json.loads(countriesFile.readline())

    for countryProperties in countriesProperties:
        countryObject = country.loadFromRefined(countryProperties)
        countries[countryObject.getName()] = countryObject

    countriesFile.close()

def getCountries():
    if len(countries) == 0:
        raise Exception("Countries data have not been initialized !")
    return countries

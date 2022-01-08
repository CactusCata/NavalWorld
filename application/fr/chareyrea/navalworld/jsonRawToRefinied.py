import json
import os
from country.country import Country
import country.country as country

def groupText(file):
    sentence = ""
    for line in file.readlines():
        sentence += line.rstrip()
    return sentence

if __name__ == "__main__":

    rawJsonFileName = "cntry08.geojson"

    if not os.path.isfile(rawJsonFileName):
        print(f"the file {rawJsonFileName} doesn't exist !")
        exit(-1)

    rawJsonFile = open(rawJsonFileName, "r")

    dictFile = json.loads(groupText(rawJsonFile))

    countries = []
    for countryProperties in dictFile["features"]:
        countryName = countryProperties["properties"]["CNTRY_NAME"]
        countries.append(country.loadFromRaw(countryName, countryProperties["geometry"]["coordinates"]).toJsonObject())

    refinedJsonFile = open("countries.geojson", 'w')
    refinedJsonFile.write(json.dumps(countries))
    rawJsonFile.close()
    refinedJsonFile.close()
    print("Done")

import utils.db.DDBUtils as DDBUtils
import random
import utils.db.DDBConnectionLoader as DDBConnectionLoader

if __name__ == "__main__":

    DDBConnectionLoader.createConnection()

    countryIDs = DDBUtils.prepareRequest(f"""
        SELECT Country.country_id
        FROM Country;
    """, 1)

    for countryID_IN in countryIDs:
        countryID_in = countryID_IN[0]
        for countryID_OUT in countryIDs:
            countryID_out = countryID_OUT[0]
            DDBUtils.updateRequest(f"""
                UPDATE Country_Affection
                SET score = {random.randint(5, 95)}
                WHERE Country_Affection.country_id_in = {countryID_in}
                AND Country_Affection.country_id_out = {countryID_out};
            """)

    DDBConnectionLoader.closeConnection()

from tkinter import CENTER
from frame.navalFrame import NavalFrame
import utils.db.DDBUtils as DDBUtils
import re
import utils.utils as utils

class CountryAddingFrame(NavalFrame):

    def __init__(self, master, country):
        super().__init__(master, "Register new country", 650, 350)
        self.country = country
        self.master = master

        super().createLabel(0.50, 0.05, f"Edition of: {country.getName()}", fontSize=15, anchor=CENTER)

        super().createLabel(0.50, 0.13, "How many money have: ", anchor=CENTER)
        self.textBoxMoney = super().createTextBox(0.05, 0.20, width=63)

        super().createLabel(0.50, 0.35, "Surface of country: ", anchor=CENTER)
        self.textBoxDimensions = super().createTextBox(0.05, 0.40, width=63)

        super().createLabel(0.50, 0.55, "Entry a list of region with format 'name, longitude, latitude'", anchor=CENTER)

        self.textBoxRegions = super().createTextBox(0.05, 0.62, width=63, height=4)

        buttonCreating = super().createButton(0.5, 0.92, "Register country", 150, 40, self.tryToCreateCountry, anchor=CENTER)

        super().loop()

    def tryToCreateCountry(self):

        if not utils.isInt(self.textBoxMoney.get("1.0", "end-1c")):
            super().throwMessage("The money must be an integer", "Error")
            return

        if not utils.isInt(self.textBoxDimensions.get("1.0", "end-1c")):
            super().throwMessage("The surface must be an integer", "Error")
            return

        textRegions = self.textBoxRegions.get("1.0", "end-1c")

        if textRegions == "\n":
            super().throwMessage("You must register one region at least", "Error")
            return

        regionsTextArray = textRegions.split("\n")
        r = re.compile("\w+, -?\d+, -?\d+")
        for i in range(len(regionsTextArray)):
            regionText = regionsTextArray[i]
            if not r.match(regionText):
                super().throwMessage(f"The ligne {i} format is incorrect", "Error")
                return

        countryID = DDBUtils.prepareRequest(f"""
            SELECT MAX(Country.country_id)
            FROM Country;
        """, 0)[0] + 1

        DDBUtils.prepareInsert(f"""
            INSERT INTO Country(country_id, country_name, country_money, country_power, surface)
            VALUES ({countryID},
                    '{self.country.getName()}',
                     {int(self.textBoxMoney.get("1.0", "end-1c"))},
                     0,
                     {int(self.textBoxDimensions.get("1.0", "end-1c"))});
        """)


        regionID = DDBUtils.prepareRequest(f"""
            SELECT MAX(Region.region_id)
            FROM Region;
        """, 0)[0] + 1
        for regionText in regionsTextArray:
            regionInformation = regionText.split(", ")
            regionName = regionInformation[0]
            regionLat = regionInformation[1]
            regionLong = regionInformation[2]
            DDBUtils.prepareInsert(f"""
                INSERT INTO Region(region_id, region_name, latitude, longitude)
                VALUES ({regionID}, '{regionName}', {regionLat}, {regionLong});
            """)
            DDBUtils.prepareInsert(f"""
                INSERT INTO Country_Region(country_id, region_id)
                VALUES ({countryID}, {regionID});
            """)
            regionID += 1

        super().throwMessage("Country added !", "Congratulations", afterReadCallback=self.master.destroy)

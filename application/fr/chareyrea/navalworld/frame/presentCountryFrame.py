from tkinter import Toplevel, CENTER
from PIL import Image, ImageTk
import utils.db.DDBUtils as DDBUtils
from frame.boatViewRealTimeFrame import BoatViewRealTimeFrame
import utils.utils as utils
from frame.navalFrame import NavalFrame

class PresentCountryFrame(NavalFrame):

    def __init__(self, master, country):
        super().__init__(master, "Country informations", 800, 700)
        self.master = master

        countryInfo = DDBUtils.getCountryByName(country.getName())

        countryID = countryInfo[0] # Name of selected country
        self.regionID = -1

        # Affichage des informations générales du pays
        super().createLabel(0.5, 0.05, f"Country: {countryInfo[1]}", anchor=CENTER)
        super().createLabel(0.05, 0.1, f"Money:")
        super().createLabel(0.05, 0.15, f"Surface:")
        super().createLabel(0.15, 0.1, f"{countryInfo[2]}M $")
        super().createLabel(0.15, 0.15, f"{countryInfo[4]} m²")

        # Affichage des affections pour les autres pays
        countriesAffections = DDBUtils.getCountriesAffectionByID(countryID)

        self.scrollable_canvas = super().createScrollableCanvas(0.05, 0.23, 300, 300)
        for countryAffection in countriesAffections:
            countryInfo = DDBUtils.getCountryByID(countryAffection[1])
            self.scrollable_canvas.feed(f"{countryInfo[1]}: {countryAffection[2]}")

        #Combobox des regions
        regions = DDBUtils.prepareRequest(f"""
            SELECT Region.*
            FROM Region, Country_Region
            WHERE Country_Region.country_id={countryID}
            AND Country_Region.region_id=Region.region_id;
        """, 1)

        regionsNames = []
        for region in regions:
            regionsNames.append(f"{region[0]}:{region[1]}")

        #ComboBox des regions
        self.comboBoxRegion = super().createComboBox(0.40, 0.12, regionsNames, callback=self.updateRegionComboBox)

        #Combobox des Bateaux
        self.comboBoxBoat = super().createComboBox(0.40, 0.16, [], callback=self.updateBoatComboBox)

        #Label des infos du bateau
        self.labelBoatID = super().createLabel(0.40, 0.20, "")
        self.labelBoatName = super().createLabel(0.40, 0.24, "")
        self.labelBoatLat = super().createLabel(0.40, 0.28, "")
        self.labelBoatLong = super().createLabel(0.40, 0.32, "")
        self.labelBoatHealth = super().createLabel(0.40, 0.36, "")
        self.labelBoatPower = super().createLabel(0.40, 0.40, "")
        self.labelBoatCommentary = super().createLabel(0.40, 0.44, "")

        # View of the ship
        self.labelShipImage = super().createLabel(0.40, 0.50, "")

        # Button View Boat
        super().createButton(0.05, 0.8, "View ships in reel time", 250, 40, self.viewShipsOnRealTime)

        super().loop()

    def updateRegionComboBox(self, event):
        regionInComboBox = self.comboBoxRegion.get().split(":")[1]
        shipsOfRegion = DDBUtils.prepareRequest(f"""
            SELECT Batiment.batiment_id, Batiment.batiment_name
            FROM Batiment, Region
            WHERE Batiment.region_id = Region.region_id
            AND Region.region_name = '{regionInComboBox}'
        """, 1)
        arrayFormatted = []
        for e in shipsOfRegion:
            arrayFormatted.append(f"{e[0]}:{e[1]}")
        self.comboBoxBoat["values"] = arrayFormatted
        self.regionID = self.comboBoxRegion.get().split(":")[0]

    def updateBoatComboBox(self, event):
        # Update combobox
        boatID = self.comboBoxBoat.get().split(":")[0]
        shipsInfo = DDBUtils.prepareRequest(f"""
            SELECT Batiment.batiment_id, Batiment.batiment_name, Batiment.latitude, Batiment.longitude, Batiment.health, Batiment_type.max_health, Batiment_type.batiment_power, Batiment.comment
            FROM Batiment, Batiment_type
            WHERE Batiment.batiment_type_id = Batiment_type.batiment_type_id
            AND Batiment.batiment_id = {boatID};
        """, 1)[0]
        self.labelBoatID["text"] = f"ID: {shipsInfo[0]}"
        self.labelBoatName["text"] = f"name: {shipsInfo[1]}"
        self.labelBoatLat["text"] = f"latitude: {shipsInfo[2]}"
        self.labelBoatLong["text"] = f"longitude: {shipsInfo[3]}"
        self.labelBoatHealth["text"] = f"Health: {shipsInfo[4]}/{shipsInfo[5]}"
        self.labelBoatPower["text"] = f"Power: {shipsInfo[6]}"
        self.labelBoatCommentary["text"] = f"Commentary: {shipsInfo[7]}"

        # Update Image
        pictureOfShip = utils.getPictureOfShip(shipsInfo[1])

        if pictureOfShip == None:
            print(f"Can't find a ship with the name '{shipsInfo[1]}.jpg'")
            return

        shipImage = Image.open("../../../res/img/Ships/" + pictureOfShip)
        shipImage = shipImage.resize((300,300))
        shipImage = ImageTk.PhotoImage(shipImage)
        self.labelShipImage.configure(image=shipImage)
        self.labelShipImage.image = shipImage

    def viewShipsOnRealTime(self):
        if self.regionID != -1:
            BoatViewRealTimeFrame(Toplevel(self.master), self.regionID)
        else:
            super().throwMessage("Select region !", "Error")

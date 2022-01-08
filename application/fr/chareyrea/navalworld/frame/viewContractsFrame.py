from tkinter import CENTER
from PIL import Image, ImageTk
import utils.db.DDBUtils as DDBUtils
import utils.utils as utils
import frame.countryMakeContractFrame as countryMakeContractFrame
from frame.navalFrame import NavalFrame

class ViewContractsFrame(NavalFrame):

    def __init__(self, master, country):
        super().__init__(master, "View contracts", 800, 650)
        self.master = master

        self.regionID = -1
        self.shipID = -1

        self.countryInfo = DDBUtils.getCountryByName(country.getName())

        self.countryID = self.countryInfo[0] # Name of selected country

        # Affichage des informations générales du pays
        super().createLabel(0.5, 0.05, "Command ships", fontSize=17, anchor=CENTER)

        super().createLabel(0.05, 0.15, "Your money:")
        super().createLabel(0.25, 0.15, f"{self.countryInfo[2]}M $")

        super().createLabel(0.05, 0.20, "List of contracts:")

        self.contracts = DDBUtils.prepareRequest(f"""
            SELECT Contract.contract_id, Contract.minCost, Contract.maxCost, Contract.tau, Contract.r, Contract.date_creating, Country.country_id, Country.country_name, Batiment.batiment_id, Batiment.batiment_name, Country_Affection.score
            FROM Contract, Batiment, Country, Country_Region, Country_Affection
            WHERE Contract.batiment_id = Batiment.batiment_id
            AND Batiment.state = 1
            AND Contract.region_id_seller = Country_Region.region_id
            AND Country.country_id = Country_Region.country_id
            AND Country.country_id = Country_Affection.country_id_in
            AND Country_Affection.country_id_out = {self.countryID}
            AND Contract.active = 1;
        """, 1)

        self.prices = []
        for contract in self.contracts:
            self.prices.append(int(countryMakeContractFrame.sumOfFunction(100 - int(contract[10]), int(contract[1]), int(contract[2]), int(contract[3]), int(contract[4]))))

        contractsLine = []
        for i in range(len(self.contracts)):
            contract = self.contracts[i]
            price = self.prices[i]
            contractsLine.append(f"{contract[0]}: {contract[9]} ({contract[7]}) {price} M $")


        self.comboBoxContracts = super().createComboBox(0.05, 0.30, contractsLine, callback=self.updateContractsComboBox)

        # Regions to deliver
        super().createLabel(0.60, 0.10, "List of regions you can deliver:")

        regions = DDBUtils.prepareRequest(f"""
            SELECT Region.*
            FROM Region, Country_Region
            WHERE Country_Region.country_id={self.countryID}
            AND Country_Region.region_id=Region.region_id;
        """, 1)

        regionsNames = []
        for region in regions:
            regionsNames.append(f"{region[0]}:{region[1]}")

        self.comboBoxRegion = super().createComboBox(0.60, 0.20, regionsNames)

        self.labelCountryName = super().createLabel(0.05, 0.40, "")
        self.labelShipBuy = super().createLabel(0.05, 0.45, "")
        self.labelPrice = super().createLabel(0.05, 0.50, "")

        #Image of selected ship
        self.labelShipImage = super().createLabel(0.50, 0.50, "")

        # Button make contract
        self.buttonBuy = super().createButton(0.25, 0.9, "Create contract", 200, 40, self.buy)

        super().loop()

    def updateContractsComboBox(self, event):
        index = self.comboBoxContracts.current()
        contract = self.contracts[index]
        price = self.prices[index]

        self.labelCountryName["text"] = f"Name of seller: {contract[7]}"
        self.labelShipBuy["text"] = f"Ship bought : {contract[9]}"
        self.labelPrice["text"] = f"Price : {price}M $"

        # Update Image
        shipName = contract[9]
        pictureOfShip = utils.getPictureOfShip(shipName)

        if pictureOfShip == None:
            print(f"Can't find a ship with the name '{shipName}.jpg'")
            return


        shipImage = Image.open("../../../res/img/Ships/" + pictureOfShip)
        shipImage = shipImage.resize((300,300))
        shipImage = ImageTk.PhotoImage(shipImage)
        self.labelShipImage.configure(image=shipImage)
        self.labelShipImage.image = shipImage

    def buy(self):
        index = self.comboBoxContracts.current()
        contract = self.contracts[index]
        price = int(self.prices[index])

        currentMoney = int(self.countryInfo[2])

        if currentMoney < int(price):
            super().throwMessage("You need more money !", title="Error")
            return

        # Update affections
        scoreAffection = DDBUtils.prepareRequest(f"""
            SELECT Country_Affection.score
            FROM Country_Affection
            WHERE Country_Affection.country_id_in = {self.countryID}
            AND Country_Affection.country_id_out = {contract[6]};
        """, 0)[0]

        DDBUtils.updateRequest(f"""
            UPDATE Country_Affection
            SET score = {min(int(scoreAffection) * 1.1, 100)}
            WHERE Country_Affection.country_id_in = {self.countryID}
            AND Country_Affection.country_id_out = {contract[6]};
        """)

        scoreAffection = DDBUtils.prepareRequest(f"""
            SELECT Country_Affection.score
            FROM Country_Affection
            WHERE Country_Affection.country_id_in = {contract[6]}
            AND Country_Affection.country_id_out = {self.countryID};
        """, 0)[0]

        DDBUtils.updateRequest(f"""
            UPDATE Country_Affection
            SET score = {min(int(scoreAffection) * 1.1, 100)}
            WHERE Country_Affection.country_id_in = {contract[6]}
            AND Country_Affection.country_id_out = {self.countryID};
        """)

        # Add command log
        DDBUtils.prepareInsert(f"""
            INSERT INTO Command(command_id, contract_id, region_id_buyer, date_buy, price)
            VALUES
                (DEFAULT, {contract[0]}, {self.countryID}, current_timestamp, {price});
        """)

        # Add action to batiment
        regionID = self.comboBoxRegion.get().split(":")[0]
        regionLatLong = DDBUtils.prepareRequest(f"""
            SELECT Region.latitude, Region.longitude
            FROM Region
            WHERE Region.region_id = {regionID};
        """, 0)

        import deplacement.actionWalkShipTask as actionWalkShipTask
        regionLatLong = actionWalkShipTask.INSTANCE.getSeaAccessible(regionLatLong[0], regionLatLong[1])

        DDBUtils.prepareInsert(f"""
            INSERT INTO Action_Batiment(action_id, batiment_id, goalLat, goalLong)
            VALUES
                (DEFAULT, {contract[8]}, {regionLatLong[0]}, {regionLatLong[1]});
        """)

        # Update contract ID
        DDBUtils.prepareDelete(f"""
            UPDATE Contract
            SET active = 0
            WHERE Contract.contract_id = {contract[0]};
        """)

        # Update batiement values
        DDBUtils.updateRequest(f"""
            UPDATE Batiment
            SET region_id = {regionID},
                state = 0
            WHERE Batiment.batiment_id = {contract[8]};
        """)

        # Reduce money country
        DDBUtils.updateRequest(f"""
            UPDATE Country
            SET country_money = {currentMoney - price}
            WHERE Country.country_id = {self.countryID}
        """)

        # Add money country
        countrySellerMoney = DDBUtils.prepareRequest(f"""
            SELECT Country.country_money
            FROM Country
            WHERE Country.country_id = {contract[6]};
        """, 0)[0]

        DDBUtils.updateRequest(f"""
            UPDATE Country
            SET country_money = {countrySellerMoney + price}
            WHERE Country.country_id = {contract[6]};
        """)

        actionWalkShipTask.INSTANCE.addDeplacement(contract[0], contract[8], regionLatLong[0], regionLatLong[1])
        super().throwMessage("You bought a ship !", title="Congratulations", afterReadCallback=self.master.destroy)

from tkinter import CENTER, BOTTOM, BOTH
from PIL import Image, ImageTk
import utils.db.DDBUtils as DDBUtils
import math
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import utils.utils as utils
from frame.navalFrame import NavalFrame

class CountryMakeContractFrame(NavalFrame):

    def __init__(self, master, country):
        super().__init__(master, "New Contract", 800, 650)

        self.regionID = -1
        self.shipID = -1

        countryInfo = DDBUtils.getCountryByName(country.getName())

        countryID = countryInfo[0] # Name of selected country

        # Affichage des informations générales du pays
        super().createLabel(0.5, 0.05, f"Country: {countryInfo[1]}", fontSize=17, anchor=CENTER)
        super().createLabel(0.02, 0.10, f"Country money:")
        super().createLabel(0.23, 0.10, f"{countryInfo[2]}M$")

        # Regions
        super().createLabel(0.02, 0.15, "Choose a region:")

        regions = DDBUtils.prepareRequest(f"""
            SELECT Region.*
            FROM Region, Country_Region
            WHERE Country_Region.country_id={countryID}
            AND Country_Region.region_id=Region.region_id;
        """, 1)

        regionsNames = []
        for region in regions:
            regionsNames.append(f"{region[0]}:{region[1]}")

        self.comboBoxRegion = super().createComboBox(0.23, 0.15, regionsNames, callback=self.updateRegionComboBox)

        # Combo box des bateaux de la region
        super().createLabel(0.02, 0.2, "Choose a ship:")
        self.comboBoxShipsAvaibles = super().createComboBox(0.23, 0.20, [], callback=self.updateShipsComboBox)

        # text area pour la valeur min (par défaut la valeur de création du type de bateau sélectionné)
        super().createLabel(0.02, 0.25, "Minimal cost:")
        self.textBoxMoneyMin = super().createTextBox(0.23, 0.25, text="0", binds={"<ButtonRelease-1>": self.updateScale, "<KeyRelease>": self.updateScale})

        super().createLabel(0.02, 0.30, "Maximal cost:")
        self.textBoxMoneyMax = super().createTextBox(0.23, 0.30, text="0", binds={"<ButtonRelease-1>": self.updateScale, "<KeyRelease>": self.updateScale})

        #Image of selected ship
        self.labelShipImage = super().createLabel(0.05, 0.38, "")

        # Button make contract
        super().createButton(0.25, 0.9, "Create contract", 200, 40, self.makeContract)

        # Scales to tau and r
        self.scaleTau = super().createScalebar(0.57, 0.10, "Tau", "horizontal", 1, 50, 300, defaultValue=4, callback=self.updateScale)
        self.scaleR = super().createScalebar(0.57, 0.25, "R", "horizontal", -30, 30, 300, defaultValue=0, callback=self.updateScale)

        self.frameFigure = super().createFrame(0.53, 0.45, 100, 100)

        # Figure Frame
        self.initFunction()

        super().loop()

    def updateRegionComboBox(self, event):
        self.regionID = self.comboBoxRegion.get().split(":")[0]
        shipsOfRegion = DDBUtils.prepareRequest(f"""
            SELECT Batiment.batiment_id, Batiment.batiment_name
            FROM Batiment, Region
            WHERE Batiment.region_id = Region.region_id
            AND Region.region_id = '{self.regionID}'
            AND Batiment.state = 0;
        """, 1)
        self.comboBoxShipsAvaibles["values"] = convertRequestToArrayStringFormat(shipsOfRegion)

    def updateShipsComboBox(self, event):
        self.shipID = int(self.comboBoxShipsAvaibles.get().split(":")[0])

        costOfShipProduction = DDBUtils.prepareRequest(f"""
            SELECT Batiment_type.costOfProductionInMillions
            FROM Batiment, Batiment_type
            WHERE Batiment.batiment_id = {self.shipID}
            AND Batiment.batiment_type_id = Batiment_type.batiment_type_id;
        """, 0)[0]

        costOfShipProduction = int(costOfShipProduction)

        self.textBoxMoneyMin.delete(1.0, "end")
        self.textBoxMoneyMin.insert(1.0, str(int(1.1 * costOfShipProduction)))

        self.textBoxMoneyMax.delete(1.0, "end")
        self.textBoxMoneyMax.insert(1.0, str(int(2 * costOfShipProduction)))

        self.drawFunction()

        # Update Image
        shipName = self.comboBoxShipsAvaibles.get().split(":")[1]
        pictureOfShip = utils.getPictureOfShip(shipName)

        if pictureOfShip == None:
            print(f"Can't find a ship with the name '{shipName}.jpg'")
            return

        shipImage = Image.open("../../../res/img/Ships/" + pictureOfShip)
        shipImage = shipImage.resize((300,300))
        shipImage = ImageTk.PhotoImage(shipImage)
        self.labelShipImage.configure(image=shipImage)
        self.labelShipImage.image = shipImage

    def updateScale(self, event):
        self.drawFunction()

    def makeContract(self):

      DDBUtils.updateRequest(f"""
        UPDATE Batiment
        SET state = 1
        WHERE Batiment.batiment_id = {self.shipID};
      """)

      DDBUtils.prepareInsert(f"""
        INSERT INTO Contract(contract_id, region_id_seller, batiment_id, minCost, maxCost, tau, r, date_creating, active)
        VALUES
            (DEFAULT, {self.regionID}, {self.shipID}, {self.textBoxMoneyMin.get("1.0", "end")}, {self.textBoxMoneyMax.get("1.0", "end")}, {self.scaleTau.get()}, {self.scaleR.get()}, current_timestamp, 1);
      """)

      super().throwMessage("Contract added !", afterReadCallback=super().closingCallbackEvent)

    def initFunction(self):
        self.figure = Figure(figsize=(3.6, 3.6), dpi=100)
        self.subPlot = self.figure.add_subplot(111)
        self.drawFigureCount = 0

    def drawFunction(self):

        if self.drawFigureCount != 0:
            self.subPlot.clear()

        minCost = int(self.textBoxMoneyMin.get("1.0", "end"))
        maxCost = int(self.textBoxMoneyMax.get("1.0", "end"))
        tau = self.scaleTau.get()
        r = self.scaleR.get()
        domainOfDefinition = [x for x in range(1, 100)]

        aboveImages = []
        underImages = []
        sumOfImages = []

        for x in domainOfDefinition:
            aboveImages.append(aboveFunction(x, minCost, maxCost, tau))
            underImages.append(underFunction(x, minCost, maxCost, tau))
            sumOfImages.append(sumOfFunction(x, minCost, maxCost, tau, r))

        self.subPlot.plot(domainOfDefinition, aboveImages, label='Max')
        self.subPlot.plot(domainOfDefinition, underImages, label='Min')
        self.subPlot.plot(domainOfDefinition, sumOfImages, label='Yours')
        #self.subPlot.set_xlabel("100 - affection") Not enought place
        #self.subPlot.set_ylabel("Cost in million of $") Not enought place
        self.subPlot.legend()

        if self.drawFigureCount == 0:
            self.canvasFigure = FigureCanvasTkAgg(self.figure, self.frameFigure)
            self.toolbar = NavigationToolbar2Tk(self.canvasFigure, self.frameFigure)


        self.canvasFigure.draw()
        self.canvasFigure.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        self.toolbar.update()

        if self.drawFigureCount == 0:
            self.canvasFigure._tkcanvas.pack()

        self.drawFigureCount += 1

def aboveFunction(x, minCost, maxCost, tau):
    return minCost + (maxCost - minCost) * math.exp(-(tau/1.1**x))

def underFunction(x, minCost, maxCost, tau):
    return maxCost + minCost - aboveFunction(-x + 100, minCost, maxCost, tau)

def sumOfFunction(x, minCost, maxCost, tau, r):
    return (1.1**r * aboveFunction(x, minCost, maxCost, tau) + 1.1**(-r) * underFunction(x, minCost, maxCost, tau))/(1.1**r + 1.1**(-r))

def convertRequestToArrayStringFormat(requestRes):
    arrayFormatted = []
    for e in requestRes:
        arrayFormatted.append(f"{e[0]}:{e[1]}")
    return arrayFormatted

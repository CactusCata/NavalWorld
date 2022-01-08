from tkinter import Canvas, Toplevel, CENTER
from frame.countrySelectionFrame import CountrySelectionFrame
from frame.presentCountryFrame import PresentCountryFrame
from frame.countryAddingFrame import CountryAddingFrame
from frame.countryMakeContractFrame import CountryMakeContractFrame
from frame.viewContractsFrame import ViewContractsFrame
from frame.navalFrame import NavalFrame
import utils.tkinterUtils as tkinterUtils
from deplacement.actionWalkShipTask import WalkerShip

class MainFrame(NavalFrame):

    def __init__(self, master):
        super().__init__(master, "Menu", 1100, 619)
        self.master = master
        self.canvas = Canvas(self.master, width=1100, height=619)
        tkinterUtils.initComboBoxStyle()

        super().enableCanvas()
        super().setBackgroundImage("../../../res/img/menu.jpg", resize=(1100, 619))

        super().createLabel(0.5, 0.1, "Naval World", fontSize=20, anchor=CENTER)

        super().createButton(0.5, 0.35, "View country", 150, 40, self.selectCountry, anchor=CENTER)
        super().createButton(0.5, 0.50, "Add new Country", 150, 40, self.addNewCountry, anchor=CENTER)
        super().createButton(0.5, 0.65, "Create contract", 150, 40, self.makeContract, anchor=CENTER)
        super().createButton(0.5, 0.80, "View contracts", 150, 40, self.viewContracts, anchor=CENTER)

        WalkerShip(self.canvas)

        super().loop()

    def selectCountry(self):
        CountrySelectionFrame(Toplevel(self.master), self.onCountryInfoSelection, 1)

    def onCountryInfoSelection(self, country):
        PresentCountryFrame(Toplevel(self.master), country)

    # ---------

    def addNewCountry(self):
        CountrySelectionFrame(Toplevel(self.master), self.onCountryAddingSelection, 0)

    def onCountryAddingSelection(self, country):
        CountryAddingFrame(Toplevel(self.master), country)

    # --------

    def makeContract(self):
        CountrySelectionFrame(Toplevel(self.master), self.onCountryMakeContractSelection, 1)

    def onCountryMakeContractSelection(self, country):
        CountryMakeContractFrame(Toplevel(self.master), country)

    # ---------

    def viewContracts(self):
        CountrySelectionFrame(Toplevel(self.master), self.onCountryViewContractSelection, 1)

    def onCountryViewContractSelection(self, country):
        ViewContractsFrame(Toplevel(self.master), country)

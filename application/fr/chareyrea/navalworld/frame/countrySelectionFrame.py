from tkinter import CENTER
from shapely.geometry.polygon import Polygon
from shapely.geometry.polygon import Point
import country.jsonRefinedReader as jsonRefinedReader
import utils.db.DDBUtils as DDBUtils
from frame.navalFrame import NavalFrame

class CountrySelectionFrame(NavalFrame):

    """
    mode = 1 --> not able to select unrenseigned country
    mode = 0 --> can select unrenseigned country
    """

    def __init__(self, master, nextStep, mode):
        super().__init__(master, "Select a country", 1160, 900, binds={"<Button-1>": self.leftClickEvent})
        self.closedWindows = False
        self.nextStep = nextStep
        self.mode = mode

        super().enableCanvas()
        super().setBackgroundImage("../../../res/img/world_map.jpg")
        super().createLabel(0.5, 0.1, "Choose a country", anchor=CENTER)

        super().setClosingCallback(self.onClosingEvent)
        super().loop()

    def onClosingEvent(self):
        self.closedWindows = True

    def leftClickEvent(self, event):
        if not self.closedWindows:
            countriesClicked = self.detectCountryOnClick(event.x, event.y)
            if len(countriesClicked) != 0:
                self.clickCountryEvent(countriesClicked[0])

    def detectCountryOnClick(self, xClicked, yClicked):
        countriesFiltered = []
        for country in jsonRefinedReader.getCountries().values():
            upLeftPoint = country.getUpLeftPoint()
            downRightPoint = country.getDownRightPoint()
            if upLeftPoint[0] < xClicked < downRightPoint[0] and downRightPoint[1] < yClicked < upLeftPoint[1]:
                for poly in country.getArrayOfPolygon():
                    if poly.contains(Point(xClicked, yClicked)):
                        countriesFiltered.append(country)
        return countriesFiltered

    def clickCountryEvent(self, countryClicked):
        if self.mode == 1:
            amount = DDBUtils.prepareRequest(f"""
                SELECT COUNT(*)
                FROM Country
                WHERE Country.country_name = '{countryClicked.getName()}';
            """, 0)[0]

            if amount == 0: # Coutry is not renseigned, avort the presentation of country
                super().throwMessage("The country that was selectionned have no informations for now.\nYou can add an entry on main menu", "Error")
            else:
                super().close()
                self.nextStep(countryClicked)
        elif self.mode == 0:
            countryExist = DDBUtils.prepareRequest(f"""
                SELECT COUNT(*)
                FROM Country
                WHERE Country.country_name = '{countryClicked.getName()}';
            """, 0)[0]

            if countryExist == 1:
                super().throwMessage("This country already exist !", title="Error")
            else:
                super().close()
                self.nextStep(countryClicked)

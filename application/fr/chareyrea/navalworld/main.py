import utils.db.DDBConnectionLoader as DDBConnectionLoader
from frame.mainFrame import MainFrame
import country.jsonRefinedReader as jsonRefinedReader
import tkinter
import cProfile
from pstats import Stats

DEBUG_MODE = False

def start():
    DDBConnectionLoader.createConnection()
    jsonRefinedReader.loadCountries()
    root = tkinter.Tk("Naval_Group BBD")
    mainFrame = MainFrame(root)
    DDBConnectionLoader.closeConnection()

def startGame(runMethod, isDebugMode):

    if isDebugMode:
        with cProfile.Profile() as pr:
            runMethod()

        Stats(pr).dump_stats(filename='profiling.prof')
    else:
        runMethod()

if __name__ == "__main__":
    startGame(start, DEBUG_MODE)

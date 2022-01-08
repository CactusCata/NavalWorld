from tkinter import CENTER
from frame.navalFrame import NavalFrame

class ErrorFrame(NavalFrame):

    def __init__(self, master, message, title="Message", nextStep=None):
        super().__init__(master, title, 900, 200)

        if (nextStep != None):
            super().setClosingCallback(nextStep)

        super().createLabel(0.5, 0.1, message, fontSize=20, anchor=CENTER)
        super().loop()

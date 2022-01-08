from tkinter import Label, Text, Scale, Canvas, Toplevel, CENTER, NW, Frame, ttk
from tkinter.ttk import Combobox
from libs.tkinter_custom_button import TkinterCustomButton
from libs.scrollableCanvas import ScrollableCanvas
from PIL import Image, ImageTk
import utils.screenUtils as screenUtils

class NavalFrame:

    def __init__(self, master, name, dimX, dimY, binds={}):
        self.master = master
        self.dimX = dimX
        self.dimY = dimY
        self.master.minsize(dimX, dimY)
        self.master.maxsize(dimX, dimY)
        xScreenPos = max(0, screenUtils.screenSize[0] // 2 - dimX // 2)
        yScreenPos = max(0, screenUtils.screenSize[1] // 2 - dimY // 2)
        self.master.geometry(f"{dimX}x{dimY}+{xScreenPos}+{yScreenPos}")
        self.master.iconbitmap('../../../res/img/icon.ico')
        self.master.title(name)
        self.master.configure(background='#1E1E1E')
        self.master.protocol("WM_DELETE_WINDOW", self.closingCallbackEvent)
        self.closingCallback = None
        self.canvas = None
        for eventName, callback in binds.items():
            self.master.bind_all(eventName, callback)

    def setClosingCallback(self, callback):
        self.closingCallback = callback

    def closingCallbackEvent(self):
        if self.closingCallback != None:
            self.closingCallback()
        self.master.destroy()

    def createLabel(self, relX, relY, text, fontSize=15, anchor=NW):
        label = Label(self.master, text=text, bg='#1E1E1E', fg='#ABB2B9', font=("Arial", fontSize))
        label.place(relx=relX, rely=relY, anchor=anchor)
        return label

    def createTextBox(self, relX, relY, text="", width=1, height=1, fontSize=13, anchor=NW, binds={}):
        textBox = Text(self.master, width=width, height=height, bg='#1E1E1E', fg='#ABB2B9', font=("Arial", fontSize))
        textBox.place(relx=relX, rely=relY, anchor=anchor)
        textBox.insert(1.0, text)
        for eventName, callback in binds.items():
            textBox.bind(eventName, callback)
        return textBox

    def createButton(self, relX, relY, text, width, height, callback, fontSize=13, anchor=NW):
        button = TkinterCustomButton(master=self.master,
                                                bg_color="#1E1E1E",
                                                fg_color="#1E1E1E",
                                                border_color="#ABB2B9",
                                                hover_color="#566573",
                                                text_font=("Arial", fontSize),
                                                text=text,
                                                text_color="white",
                                                corner_radius=0,
                                                border_width=2,
                                                width=width,
                                                height=height,
                                                hover=True,
                                                command=callback)
        button.place(relx=relX, rely=relY, anchor=anchor)
        return button

    def createScalebar(self, relX, relY, text, orientation, from_, to, length, defaultValue=None, tickInterval=10, callback=None, resolution=1, fontSize=13):
        if defaultValue == None:
            defaultValue = from_
        scalebar = Scale(self.master, orient=orientation, from_=from_, to=to, resolution=resolution, tickinterval=tickInterval, length=length, label=text, bg='#1E1E1E', fg='#ABB2B9', font=("Arial", fontSize))
        if callback != None:
            scalebar.bind("<ButtonRelease-1>", callback)
        scalebar.set(defaultValue)
        scalebar.place(relx=relX, rely=relY)
        return scalebar


    def createComboBox(self, relX, relY, list, fontSize=15, callback=None):
        comboBox = Combobox(self.master, values=list)
        comboBox.configure(font=("Arial", fontSize))
        comboBox.place(relx=relX, rely=relY)

        if (callback != None):
            comboBox.bind("<<ComboboxSelected>>", callback)

        return comboBox

    def createScrollableCanvas(self, relX, relY, width, height):
        frameScrollableCanvas = self.createFrame(relX, relY, width, height)
        scrollableCanvas = ScrollableCanvas(frameScrollableCanvas, background='#1E1E1E')
        scrollableCanvas.grid(row=1,column=1)
        scrollableCanvas.configure(bg='#1E1E1E')
        return scrollableCanvas

    def createFrame(self, relX, relY, width, height):
        frame = Frame(self.master, width=width, height=height, bg='#1E1E1E')
        frame.place(relx=relX, rely=relY)
        return frame

    def enableCanvas(self):
        self.canvas =  Canvas(self.master, width=self.dimX, height=self.dimY)
        self.canvas.pack()

    def setBackgroundImage(self, path, resize=None):
        if self.canvas == None:
            print("Need to enable canvas")
            return

        image = Image.open(path)
        if resize != None:
            image = image.resize((resize[0], resize[1]), Image.ANTIALIAS)

        self.backgroundImage = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.backgroundImage)

    def drawCircle(self, x, y, r):
        if self.canvas == None:
            print("Need to enable canvas")
            return None
        return self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='white')

    def deleteForm(self, form):
        self.canvas.delete(form)

    def scheduleTask(self, time, task):
        self.master.after(time, task)

    def loop(self):
        self.master.mainloop()

    def close(self):
        self.closingCallbackEvent()

    def throwMessage(self, message, title="Message", afterReadCallback=None):
        from frame.errorFrame import ErrorFrame
        ErrorFrame(Toplevel(self.master), message, title=title, nextStep=afterReadCallback)

from tkinter import *

class ScrollableCanvas(Frame):

    def feed(self, text):
        l = Label(self.interior, text=text, bg='#1E1E1E', fg='#ABB2B9', font=("Arial", 15))
        l.pack()

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        super().config(bg='#1E1E1E')

        canvas=Canvas(self,bg='#1E1E1E',width=300,height=300,scrollregion=(0,0,500,500))

        vbar=Scrollbar(self,orient=VERTICAL, bg='#1E1E1E')
        vbar.pack(side=RIGHT, fill=Y)
        vbar.config(command=canvas.yview)

        canvas.config(width=200,height=200)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=LEFT,expand=True,fill=BOTH)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas, bg='#1E1E1E')
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

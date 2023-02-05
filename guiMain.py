import tkinter as tk
from tkinter import ttk

LARGEFONT = ("Verdana", 35)


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="RLC-Circuit simulator", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Page 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row=1, column=1, padx=10, pady=10)


# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Enter Values", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))
        button2 = ttk.Button(self, text="Start",
                             command=lambda: controller.show_frame(StartPage))
        button1.grid(row=3, column=3, padx=10, pady=10)
        button2.grid(row=3, column=4, padx=10, pady=10)

        tk.Label(self, text="Va").grid(row=1)
        tk.Label(self, text="f").grid(row=2)
        tk.Label(self, text="R1").grid(row=3)
        tk.Label(self, text="L1").grid(row=4)
        tk.Label(self, text="C1").grid(row=5)
        tk.Label(self, text="").grid(row=6)

        e1 = tk.Entry(self)
        e2 = tk.Entry(self)
        e3 = tk.Entry(self)
        e4 = tk.Entry(self)
        e5 = tk.Entry(self)
        e6 = tk.Entry(self)

        e1.grid(row=1, column=1)
        e2.grid(row=2, column=1)
        e3.grid(row=3, column=1)
        e4.grid(row=4, column=1)
        e5.grid(row=5, column=1)
        e6.grid(row=6, column=1)


# Driver Code
app = tkinterApp()
app.mainloop()

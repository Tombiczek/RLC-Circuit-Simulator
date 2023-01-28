import tkinter as tk


def main():
    def New_Window():
        Window = tk.Toplevel()
        canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)
        canvas.pack()

    HEIGHT = 500
    WIDTH = 700

    ws = tk.Tk()
    ws.title("RLC Circuit Simulator")
    canvas = tk.Canvas(ws, height=HEIGHT, width=WIDTH)
    canvas.pack()

    button_series = tk.Button(ws, text="Series", bg='White', fg='Black',
                       command=lambda: New_Window())

    button_parallel = tk.Button(ws, text="Parallel", bg='White', fg='Black',
                       command=lambda: New_Window())

    button_series.place(x=120, y=140)
    button_parallel.place(x=380, y=140)

    ws.mainloop()


if __name__ == '__main__':
    main()

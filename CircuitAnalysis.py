import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.pyplot import semilogx
from matplotlib import pyplot

import PySpice.Logging.Logging as Logging

logger = Logging.setup_logging()

from PySpice.Doc.ExampleTools import find_libraries
from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import tkinter as tk
from tkinter import ttk

from engineering_notation import EngNumber

from matplotlib.ticker import EngFormatter

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

    def Main_Circuit(v_a, f_, r_1, c_1, l_1):
        circuit = Circuit('Series RLC Circuit')

        # Define amplitude and frequency of input sinusoid
        Va = v_a
        f = f_
        Vo = 0
        Td = 0
        Df = 0

        circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd,
                                        amplitude=Va, frequency=f, offset
                                        =Vo, delay=Td, damping_factor=Df)

        # Set R = 4k for over damped, R = 2k for critically damped and R=500 for under damped
        R1 = circuit.R(1, 'input', 'a', r_1)
        L1 = circuit.L(1, 'a', 'out', c_1)
        C1 = circuit.C(1, 'out', circuit.gnd, l_1)

        # Define transient simulation step time and stop time
        steptime = 0.1 @ u_us
        finaltime = 5 * (1 / f)

        # Simulation: Transient Analysis
        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        analysis = simulator.transient(step_time=steptime, end_time=finaltime)

        # Theory: Phasor circuit analysis

        # steady-state output voltage
        time = np.array(analysis.time)
        Vin = Va
        Z_R = circuit.R1.resistance
        Z_C = (1 / (1j * 2 * math.pi * f * circuit.C1.capacitance))
        Z_L = 1j * 2 * math.pi * f * circuit.L1.inductance

        Z_T = Z_L + Z_R + Z_C

        VL = (Z_L / Z_T) * Vin
        VR = (Z_R / Z_T) * Vin
        VC = (Z_C / Z_T) * Vin
        vC = abs(VC) * np.sin(2 * math.pi * f * time + np.angle(VC))
        vR = abs(VR) * np.sin(2 * math.pi * f * time + np.angle(VR))
        vL = abs(VL) * np.sin(2 * math.pi * f * time + np.angle(VL))

        print('----------')
        print('Impedances')
        print('----------')
        print('Resistor Impedance ={} Ω'.format(EngNumber(float(Z_R))))
        print('Capacitor Impedance = {:.2f} Ω'.format(Z_C))
        print('Inductor Impedance = {:.2f} Ω'.format(Z_L))

        alpha = float(circuit.R1.resistance / (2 * circuit.L1.inductance))
        omega0 = float(math.sqrt(1 / (circuit.L1.inductance * circuit.C1.capacitance)))
        damping_ratio = float(alpha / omega0)

        print('Alpha ={} rad/s'.format(EngNumber(alpha)))
        print('Omega_0 ={} rad/s'.format(EngNumber(omega0)))
        print('Damping ratio ={}'.format(EngNumber(damping_ratio)))

        if damping_ratio == 1:
            print('-----------------')
            print('Series RLC circuit is critically damped')
            print('-----------------')
        elif damping_ratio > 1:
            print('-----------')
            print('Series RLC circuit is overdamped')
            print('------------')
        else:
            print('-----------')
            print('Series RLC circuit is underdamped')
            print('-----------')

        # Plotting Simulation Results
        plt.style.use('dark_background')
        figure = plt.subplots(figsize=(11, 6))

        axe = plt.subplot(121)
        plt.title('Time Domain Waveforms')
        plt.xlabel('Time')
        plt.ylabel('Voltage [V]')
        plt.grid()
        formatter0 = EngFormatter(unit='s')
        axe.xaxis.set_major_formatter(formatter0)

        plot(analysis['input'], 'k')
        plot(analysis['out'], 'c')
        plt.plot(time, vC, 'c:')
        plot(analysis['input'] - analysis['a'], 'm')
        plt.plot(time, vR, 'm:')
        plot(analysis['a'] - analysis['out'], 'y')
        plt.plot(time, vL, 'y:')
        plt.legend(('sim:$v_{in}(t)$', 'sim:$v_{C}(t)$', 'theory:$v_{C}(t)$',
                    'sim:$v_{R}(t)$', 'theory:$v_{R}(t)$'
                    , 'sim:$v_{L}(t)$', 'theory:$v_{L}(t)$'), loc='lower right')
        # plt.ticklabel_format(axis="x", style="sci", scilimits=(0,0))
        cursor = Cursor(axe, useblit=True, color='red', linewidth=1)

        # Plotting Phasor Diagram

        # figure = plt.subplots(figsize=(11, 6))
        axe = plt.subplot(122)

        plt.title('Phasor Diagram for Voltages')

        axe.quiver(0, 0, float(Vin), 0, units='xy', scale=1, color='k')
        axe.quiver(0, 0, np.array((np.real(VC))), np.array((np.imag(VC))), units='xy', scale=1, color='c')
        axe.quiver(0, 0, np.array((np.real(VR))), np.array((np.imag(VR))), units='xy', scale=1, color='m')
        axe.quiver(0, 0, np.array((np.real(VL))), np.array((np.imag(VL))), units='xy', scale=1, color='y')

        plt.grid()
        axe.set_aspect('equal')
        axe.spines['left'].set_position('zero')
        axe.spines['right'].set_color('none')
        axe.spines['bottom'].set_position('zero')
        axe.spines['top'].set_color('none')

        limit = max(float(Va), np.amax(abs(VC)), np.amax(abs(VR)), np.amax(abs(VL)))
        plt.xlim(-limit, limit)
        plt.ylim(-limit, limit)
        plt.legend(('$\mathbf{V}_{in}$', '$\mathbf{V}_{C}$', '$\mathbf{V}_{R}$', '$\mathbf{V}_{L}$'))

        plt.tight_layout()
        plt.show()

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
                             command=lambda: controller.Main_Circuit(x1=e1.get()+" @ u_V", x2=e2.get()+" @ u_kHz", x3=e3.get()+" @ u_Ω",
                                                                     x4=e4.get()+" @ u_mH", x5=e5.get()+" @ u_nF"))
        button1.grid(row=3, column=3, padx=10, pady=10)
        button2.grid(row=3, column=4, padx=10, pady=10)

        tk.Label(self, text="Va").grid(row=1)
        tk.Label(self, text="f").grid(row=2)
        tk.Label(self, text="R1").grid(row=3)
        tk.Label(self, text="L1").grid(row=4)
        tk.Label(self, text="C1").grid(row=5)

        e1 = tk.Entry(self)
        e2 = tk.Entry(self)
        e3 = tk.Entry(self)
        e4 = tk.Entry(self)
        e5 = tk.Entry(self)

        e1.grid(row=1, column=1)
        e2.grid(row=2, column=1)
        e3.grid(row=3, column=1)
        e4.grid(row=4, column=1)
        e5.grid(row=5, column=1)


# Driver Code
app = tkinterApp()
app.mainloop()

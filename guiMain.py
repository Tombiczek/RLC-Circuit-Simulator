import tkinter as tk
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
    steptime = 0.1
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
    # print('Resistor Impedance ={} Ω'.format(EngNumber(float(Z_R))))
    print('Capacitor Impedance = {:.2f} Ω'.format(Z_C))
    print('Inductor Impedance = {:.2f} Ω'.format(Z_L))

    alpha = float(circuit.R1.resistance / (2 * circuit.L1.inductance))
    omega0 = float(math.sqrt(1 / (circuit.L1.inductance * circuit.C1.capacitance)))
    damping_ratio = float(alpha / omega0)

    # print('Alpha ={} rad/s'.format(EngNumber(alpha)))
    # print('Omega_0 ={} rad/s'.format(EngNumber(omega0)))
    # print('Damping ratio ={}'.format(EngNumber(damping_ratio)))

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
    # formatter0 = EngFormatter(unit='s')
    # axe.xaxis.set_major_formatter(formatter0)

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


LARGEFONT = ("Verdana", 35)

r = tk.Tk()
r.title('Counting Seconds')
label = tk.Label(text="Enter Values", font=LARGEFONT)
label.grid(row=0, column=4, padx=10, pady=10)

tk.Label(text="Va").grid(row=1)
tk.Label(text="f").grid(row=2)
tk.Label(text="R1").grid(row=3)
tk.Label(text="L1").grid(row=4)
tk.Label(text="C1").grid(row=5)

e1 = tk.Entry(r)
e2 = tk.Entry(r)
e3 = tk.Entry(r)
e4 = tk.Entry(r)
e5 = tk.Entry(r)
e1.grid(row=1, column=1)
e2.grid(row=2, column=1)
e3.grid(row=3, column=1)
e4.grid(row=4, column=1)
e5.grid(row=5, column=1)

button2 = tk.Button(text="Start", command=lambda: Main_Circuit(e1.get() + " @ u_V", e2.get() + " @ u_kHz",
                                                               e3.get() + " @ u_Ω",
                                                               e4.get() + " @ u_mH", e5.get() + " @ u_nF"))

button2.grid(row=3, column=4, padx=10, pady=10)

r.mainloop()

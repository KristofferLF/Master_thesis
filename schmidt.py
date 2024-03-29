import os
import random
from turtle import color, width
from matplotlib.axis import XAxis
from matplotlib.lines import Line2D
import numpy as np
import matplotlib.pyplot as plt
import pyqtgraph as pg
from matplotlib.backends.backend_pdf import PdfPages

def schmidtAnalysis(values):
    """
    Performs a Schmidt-analysis and returns a matrix containing the results of the analysis.
    Input: 'values' List of values used for calculation [R, m, Th_c, Tr_c, Tc_c, V_cyl, V_reg, V_c_avg, piston_rod_area, piston_cyl_area, phaseAngle_beta]
    Output: 'cycleAnalysis' Matrix of results
    """
    # Constants
    R = values[0]   # [J/kg*K]
    m = values[1]   # [kg]

    ## Temperature
    Th_c = values[2]    # [C]
    Tr_c = values[3]    # [C]
    Tc_c = values[4]    # [C]
    T_h = 273.15 + Th_c     # [K]
    T_r = 273.15 + Tr_c     # [K]
    T_c = 273.15 + Tc_c     # [K]

    ## Volume
    V_cyl = values[5]       # [mm^3]
    V_reg = values[6]       # [mm^3]
    V_c_avg = values[7]     # [mm^3]

    ## Area
    piston_rod_area = values[8]  # [mm^2]
    piston_cyl_area = values[9]  # [mm^2]

    # Angles
    beta = values[10]   # [degrees]
    beta_rad = beta * 2 * np.pi / 360

    degree = 0
    cycleAnalysis = np.zeros((37, 16))

    for i in range(37):
        cycleAnalysis[i,0] = degree         # [degrees]
        rad = degree * 2 * np.pi / 360
        cycleAnalysis[i,1] = rad            # [rad]
        V_c = V_c_avg + np.sin(rad) * V_cyl / 2
        cycleAnalysis[i,2] = V_c            # [mm^3]
        V_e = V_c_avg + np.sin(rad + beta_rad) * V_cyl / 2
        cycleAnalysis[i,3] = V_e            # [mm^3]
        V_t = (V_c + V_e) / 1000000
        cycleAnalysis[i,4] = V_t            # [dm^3]
        Sum_V_div_T = (V_c / T_c) + (V_reg / T_r) + (V_e / T_h)
        cycleAnalysis[i,5] = Sum_V_div_T    # [mm^3/K]
        P_1 = m * R * 1000 / Sum_V_div_T
        cycleAnalysis[i,6] = P_1            # [N/mm^2]

        degree += 10

    # Assigning P_2 [N/mm^2]
    cycleAnalysis[:18,7] = cycleAnalysis[19:,6]
    cycleAnalysis[18:,7] = cycleAnalysis[:19,6]

    for i in range(1,37):
        W_1 = P_1 * (cycleAnalysis[i,2] - cycleAnalysis[i-1,2]) / 1000
        cycleAnalysis[i,8] = W_1            # [Nm]
        W_2 = P_1 * (cycleAnalysis[i,3] - cycleAnalysis[i-1,3]) / 1000
        cycleAnalysis[i,9] = W_2            # [Nm]
        W_r = W_1 + W_2
        cycleAnalysis[i,10] = W_r           # [Nm]
        F_o = cycleAnalysis[i,6] * piston_cyl_area
        cycleAnalysis[i,11] = F_o           # [N]
        F_u = cycleAnalysis[i,7] * (piston_cyl_area - piston_rod_area)
        cycleAnalysis[i,12] = F_u           # [N]
        F_r = F_o - F_u
        cycleAnalysis[i,13] = F_r           # [N]

    # Assigning P_3 and P_4 [N/mm^2]
    cycleAnalysis[:29,14] = cycleAnalysis[8:,6]
    cycleAnalysis[29:,14] = cycleAnalysis[:8,6]
    cycleAnalysis[:19,15] = cycleAnalysis[18:,14]
    cycleAnalysis[18:,15] = cycleAnalysis[:19,14]
    
    return cycleAnalysis

def plotSchmidtAnalysis(resultFileName, cycleAnalysis):
    '''
    Plots results from a Schmidt-analysis. Volume, pressure, mechanical work, and forces are plotted against the number of degrees for one Stirling cycle.
    Input: 'resultFileName' String containing the desired path for a PDF containing the plots. Must not include path or '.pdf'.
    'cycleAnalysis' Numpy array containing calculated results from the Schmidt-analysis.
    '''

    # Removes result-file if it exists
    if os.path.exists("results/" + resultFileName + ".pdf"):
        os.remove("results/" + resultFileName + ".pdf")

    pdfPages = PdfPages("results/" + resultFileName + ".pdf")
    plt.figure()
    plt.clf()

    # Plot volume variation
    plt.fill_between(cycleAnalysis[:,0], cycleAnalysis[:,2] + cycleAnalysis[:,3], color='lightskyblue', label="Expansion volume", zorder=2)
    plt.fill_between(cycleAnalysis[:,0], cycleAnalysis[:,2], color='indianred', label="Compression volume", zorder=3)
    
    plt.xticks(np.arange(0, 390, 30))
    plt.xlabel("Degrees")
    plt.yticks(np.arange(0, 32500000, 2500000))
    plt.ylabel("Volume [mm3]")
    plt.title("Volume variation")
    plt.margins(x=0)
    plt.ylim(0, 30000000)
    plt.grid()
    plt.legend()

    pdfPages.savefig()

    # Plot circuit pressure
    plt.figure()
    plt.clf()

    plt.plot(cycleAnalysis[:,0], cycleAnalysis[:,6], color='b', label="P_1")
    plt.plot(cycleAnalysis[:,0], cycleAnalysis[:,7], color='r', label="P_2")
    plt.plot(cycleAnalysis[:,0], cycleAnalysis[:,14], color='g', label="P_3")
    plt.plot(cycleAnalysis[:,0], cycleAnalysis[:,15], color='y', label="P_4")

    plt.xticks(np.arange(0, 390, 30))
    plt.xlabel("Degrees")
    plt.yticks(np.arange(0, 22, 2))
    plt.ylabel("Pressure [N/mm2]")
    plt.title("Pressure variation")
    plt.margins(x=0)
    plt.ylim(0, 20)
    plt.grid()
    plt.legend()

    pdfPages.savefig()

    # Plot mechanical work
    plt.figure()
    plt.clf()

    plt.plot(cycleAnalysis[1:,0], cycleAnalysis[1:,8] / 1000, color='b', label="W_1")
    plt.plot(cycleAnalysis[1:,0], cycleAnalysis[1:,9] / 1000, color='r', label="W_2")
    plt.plot(cycleAnalysis[1:,0], cycleAnalysis[1:,10] / 1000, color='g', label="W_R")

    plt.xticks(np.arange(0, 390, 30))
    plt.xlabel("Degrees")
    plt.yticks(np.arange(-25, 25, 2.5))
    plt.ylabel("Work [kNm]")
    plt.title("Work variation")
    plt.margins(x=0)
    plt.xlim(0, 360)
    plt.ylim(-20, 20)
    plt.grid()
    plt.legend()

    pdfPages.savefig()

    # Plot piston forces
    plt.figure()
    plt.clf()

    plt.plot(cycleAnalysis[1:,0], cycleAnalysis[1:,11] / 1000, color='b', label="F_O")
    plt.plot(cycleAnalysis[1:,0], cycleAnalysis[1:,12] / 1000, color='r', label="F_U")
    plt.plot(cycleAnalysis[1:,0], cycleAnalysis[1:,13] / 1000, color='g', label="F_R")

    plt.xticks(np.arange(0, 390, 30))
    plt.xlabel("Degrees")
    plt.yticks(np.arange(-500, 1750, 250))
    plt.ylabel("Force [kN]")
    plt.title("Force variation")
    plt.margins(x=0)
    plt.xlim(0, 360)
    plt.ylim(-500, 1500)
    plt.grid()
    plt.legend()

    pdfPages.savefig()

    pdfPages.close()
    
def createSchmidtPlots(window, cycleAnalysis):
    window.canvas = pg.GraphicsLayoutWidget(size=(1000, 800))
    #window.canvas.resize(1500, 880)
    window.canvas.setBackground('w')
    
    # Set spacing of values along the x-axis
    xAxis = [
        (0, "0"),
        (60, "60"),
        (120, "120"),
        (180, "180"),
        (240, "240"),
        (300, "300"),
        (360, "360"),
    ]
    
    # Volume variation
    volumeVariation = window.canvas.addPlot(name="Volume variation", title="Volume variation")
    volumeVariation.addLegend()
    compressionCurve = pg.PlotCurveItem(x=cycleAnalysis[:,0], y=cycleAnalysis[:,2], pen=pg.mkColor(205, 92, 92), name="Compression area")
    expansionCurve = pg.PlotCurveItem(x=cycleAnalysis[:,0], y=cycleAnalysis[:,2] + cycleAnalysis[:,3], pen=pg.mkColor(135, 206, 250), name="Expansion area")
    horizontalLine = pg.PlotCurveItem(x=cycleAnalysis[:,0], y=np.zeros_like(cycleAnalysis[:,0]))
    filledCompressionArea = pg.FillBetweenItem(horizontalLine, compressionCurve, pg.mkColor(205, 92, 92))
    filledTotalArea = pg.FillBetweenItem(compressionCurve, expansionCurve, pg.mkColor(135, 206, 250))
    volumeVariation.addItem(compressionCurve)
    volumeVariation.addItem(expansionCurve)
    volumeVariation.addItem(filledCompressionArea)
    volumeVariation.addItem(filledTotalArea)
    
    volumeVariationMarker = pg.InfiniteLine(pen=pg.mkPen('k', width=3))
    volumeVariation.addItem(volumeVariationMarker)
    window.plotMarkers.append(volumeVariationMarker)
    
    volumeVariation.setXRange(0, 360, padding=0)
    volumeVariation.setYRange(0, 30000000, padding=0)
    
    volumeVariation.setLabel('bottom', "Degrees")
    volumeVariation.setLabel('left', "Volume [mm3]")
    
    volumeVariation.getAxis('bottom').setTicks([xAxis])
    
    # Circuit pressure
    circuitPressure = window.canvas.addPlot(name="Circuit pressure", title="Circuit pressure")
    circuitPressure.addLegend()
    p1 = pg.PlotCurveItem(x=cycleAnalysis[:,0], y=cycleAnalysis[:,6], pen='b', name="P_1")
    p2 = pg.PlotCurveItem(x=cycleAnalysis[:,0], y=cycleAnalysis[:,7], pen='r', name="P_2")
    p3 = pg.PlotCurveItem(x=cycleAnalysis[:,0], y=cycleAnalysis[:,14], pen='g', name="P_3")
    p4 = pg.PlotCurveItem(x=cycleAnalysis[:,0], y=cycleAnalysis[:,15], pen='y', name="P_4")
    circuitPressure.addItem(p1)
    circuitPressure.addItem(p2)
    circuitPressure.addItem(p3)
    circuitPressure.addItem(p4)
    
    circuitPressureMarker = pg.InfiniteLine(pen=pg.mkPen('k', width=3))
    circuitPressure.addItem(circuitPressureMarker)
    window.plotMarkers.append(circuitPressureMarker)
    
    circuitPressure.setXRange(0, 360, padding=0)
    circuitPressure.setYRange(0, 20, padding=0)
    
    circuitPressure.setLabel('bottom', "Degrees")
    circuitPressure.setLabel('left', "Pressure [N/mm2]")
    
    circuitPressure.getAxis('bottom').setTicks([xAxis])
    
    # Mechanical work
    mechanicalWork = window.canvas.addPlot(name="Mechanical work", title="Mechanical work", row=2, col=0)
    mechanicalWork.addLegend()
    w1 = pg.PlotCurveItem(x=cycleAnalysis[1:,0], y=cycleAnalysis[1:,8] / 1000, pen='b', name="W_1")
    w2 = pg.PlotCurveItem(x=cycleAnalysis[1:,0], y=cycleAnalysis[1:,9] / 1000, pen='r', name="W_2")
    w3 = pg.PlotCurveItem(x=cycleAnalysis[1:,0], y=cycleAnalysis[1:,10] / 1000, pen='g', name="W_3")
    mechanicalWork.addItem(w1)
    mechanicalWork.addItem(w2)
    mechanicalWork.addItem(w3)
    
    mechanicalWorkMarker = pg.InfiniteLine(pen=pg.mkPen('k', width=3))
    mechanicalWork.addItem(mechanicalWorkMarker)
    window.plotMarkers.append(mechanicalWorkMarker)
    
    mechanicalWork.setXRange(0, 360, padding=0)
    mechanicalWork.setYRange(-20, 20, padding=0)
    
    mechanicalWork.setLabel('bottom', "Degrees")
    mechanicalWork.setLabel('left', "Work [kNm]")
    
    mechanicalWork.getAxis('bottom').setTicks([xAxis])
    
    # Piston forces
    pistonForces = window.canvas.addPlot(x=cycleAnalysis[1:,0], y=cycleAnalysis[1:,11] / 1000, name="PistonForces", title="PistonForces", row=2, col=1)
    pistonForces.addLegend()
    fo = pg.PlotCurveItem(x=cycleAnalysis[1:,0], y=cycleAnalysis[1:,11] / 1000, pen='b', name="F_O")
    fu = pg.PlotCurveItem(x=cycleAnalysis[1:,0], y=cycleAnalysis[1:,12] / 1000, pen='r', name="F_U")
    fr = pg.PlotCurveItem(x=cycleAnalysis[1:,0], y=cycleAnalysis[1:,13] / 1000, pen='g', name="F_R")
    pistonForces.addItem(fo)
    pistonForces.addItem(fu)
    pistonForces.addItem(fr)
    
    pistonForcesMarker = pg.InfiniteLine(pen=pg.mkPen('k', width=3))
    pistonForces.addItem(pistonForcesMarker)
    window.plotMarkers.append(pistonForcesMarker)
    
    pistonForces.setXRange(0, 360, padding=0)
    pistonForces.setYRange(-500, 1500, padding=0)
    
    pistonForces.setLabel('bottom', "Degrees")
    pistonForces.setLabel('left', "Force [kN]")
    
    pistonForces.getAxis('bottom').setTicks([xAxis])
    
    #window.canvas.ci.layout.setRowStretchFactor(0, 4)
    #window.canvas.ci.layout.setRowStretchFactor(1, 1)
    #window.canvas.ci.layout.setColumnStretchFactor(0, 1)
    #window.canvas.ci.layout.setColumnStretchFactor(1, 1)
    #window.canvas.ci.layout.setColumnMaximumWidth(0,100)
    #window.canvas.ci.layout.setColumnMaximumWidth(1,100)
    window.canvas.ci.layout.setContentsMargins(10, 0, 30, 10)
import pandas as pds
import math
import numpy as np
import matplotlib.pyplot as plt


# 1.GLOBAL VARIABLES
no_of_cycles = 100 # The value is recalculated from logged data

EnocderZ_Offset = 1  # Angle after which the exact Rotor 0deg occurs after Encoder Z signal [ Always positive ]
                      ########### Input from GUI
Calibration_Multiplier = 10   # Pressure sensor calibration bar/volt
Calibration_Offset = 0        # Y intercept of calibration curve bar
# Duration for which Pressure Sensor 1 is open to intake manifold
# Intake Manifold pressure will be equated to average P1 pressure in this duration for pegging
InletValve_open = 10
InletValve_close = 30
# Duration for which Pressure Sensor 1 & 2 is open to same part of expansion chamber
# Avg pressure in this duration will be equated for both sensor
P1P2_open = 125
P1P2_close = 130
P1P2_middle = math.floor(0.5 * (P1P2_open+P1P2_close))

Intake_Manifold_pressure = 30  ########### Input from GUI
Avg_ManifoldOverlapPeriod_Pressure1 = 0 # Avg pressure of sensor 1 during intake manifold overlap duration
Avg_overlapPeriod_Pressure1 = 0 # Avg pressure of sensor 1 during sensors overlap duration
Avg_overlapPeriod_Pressure2 = 0 # Avg pressure of sensor 2 during sensors overlap duration

# 2. READING RAW DATA FROM CSV FILE
filename ='G:/Engine_DAQ_vi/EngineEdgeTrigger/teensy5.csv'

rawDataDataFrame = pds.read_csv(filename, header=0)
rawData = rawDataDataFrame.to_numpy()
#numrows_rawData = 16406
numrows_rawData = rawData.shape[0]
numcols_rawData = rawData.shape[1]
#no_of_cycles = math.floor((5468 - EnocderZ_Offset ) /360 ) # Recalculating no of cycles logged from last rotor angle stored

no_of_cycles = math.floor((rawData[numrows_rawData-1 , 0] - EnocderZ_Offset ) /360 ) # Recalculating no of cycles logged from last rotor angle stored

Pressure1_volt  = np.zeros(( 360*3, no_of_cycles))
Pressure2_volt  = np.zeros(( 360*3, no_of_cycles))

Pressure1_bar_0_33  = np.zeros(( 360*3, no_of_cycles))
Pressure2_bar_0_33  = np.zeros(( 360*3, no_of_cycles))

Pressure1_bar_1deg  = np.zeros((361, no_of_cycles))  # 0 to 360 deg is stored
Pressure2_bar_1deg  = np.zeros((361, no_of_cycles))

Pressure1_bar_pegged  = np.zeros((361, no_of_cycles))
Pressure2_bar_pegged  = np.zeros((361, no_of_cycles))
PressureCombined_bar  = np.zeros((361, no_of_cycles))

#Pressure1 = [[0 for x in range(no_of_cycles)] for y in range(360*3)]
# a = [[0 for x in range(columns)] for y in range(rows)]

# 3.CONVERTING SINGLE COLUMN DATA INTO COLUMNS FOR EACH CYCLE
# (EnocderZ_Offset,no_of_cycles*360*3)
# iterate through rows
for row in range(0, (360*3)):
    # iterate through columns
    for cycle in range(0, no_of_cycles):
        index_rawData = EnocderZ_Offset + row + cycle*360*3
        Pressure1_volt[row, cycle] = rawData[index_rawData, 1]  # Second column in rawData is press 1
        Pressure2_volt[row, cycle] = rawData[index_rawData, 2]  # Third column in rawData is press 2
        Pressure1_bar_0_33[row, cycle] = Calibration_Offset + Pressure1_volt[row, cycle] * Calibration_Multiplier
        Pressure2_bar_0_33[row, cycle] = Calibration_Offset + Pressure2_volt[row, cycle] * Calibration_Multiplier

# 4. PEGGING
  # 4a. CONVERTING ALL DATA TO POSITIVE VALUE
# Get the minimum values of each column i.e. along axis 0
minInColumns1 = np.amin(Pressure1_bar_0_33, axis=0)
minInColumns2 = np.amin(Pressure2_bar_0_33, axis=0)
# iterate through columns
for cycle in range(0, no_of_cycles):
    # iterate through rows
    for row in range(0, (360 * 3)):
        # Substracting column wise minimum value to remove negative values
        Pressure1_bar_0_33[row, cycle] = Pressure1_bar_0_33[row, cycle] - minInColumns1[cycle]
        Pressure2_bar_0_33[row, cycle] = Pressure2_bar_0_33[row, cycle] - minInColumns2[cycle]
# 4b. BINNING TO REDUCE RESOLUTION FROM 0.33 deg to 1deg by three point central averaging
# iterate through columns
for cycle in range(0, no_of_cycles):
    # iterate through rows
    for row in range(1, 360):
        Pressure1_bar_1deg[row, cycle] = 0.33 * (Pressure1_bar_0_33[3*row - 1, cycle] + Pressure1_bar_0_33[3*row, cycle] + Pressure1_bar_0_33[3*row + 1, cycle])
        Pressure2_bar_1deg[row, cycle] = 0.33 * (Pressure2_bar_0_33[3 * row - 1, cycle] + Pressure2_bar_0_33[3 * row, cycle] + Pressure2_bar_0_33[3 * row + 1, cycle])
    # @ angle 0 forward avg
    Pressure1_bar_1deg[0, cycle] = 0.5 * (Pressure1_bar_0_33[0, cycle]+ Pressure1_bar_0_33[1, cycle])
    # @ angle 360 backward avg
    Pressure1_bar_1deg[360, cycle] = 0.5 * (Pressure1_bar_0_33[360*3-2, cycle] + Pressure1_bar_0_33[360*3-1, cycle])
    Pressure2_bar_1deg[0, cycle] = 0.5 * (Pressure2_bar_0_33[0, cycle]+ Pressure2_bar_0_33[1, cycle])
    Pressure2_bar_1deg[360, cycle] = 0.5 * (Pressure2_bar_0_33[360 * 3 - 2, cycle] + Pressure2_bar_0_33[360 * 3 -1, cycle])

# 4cur. PEGGING

Avg_ManifoldOverlapPeriod_Pressure1 = np.mean(Pressure1_bar_1deg [InletValve_open: InletValve_close, :], axis=0)

# iterate through columns
for cycle in range(0, no_of_cycles):
    Pressure1_bar_pegged[:, cycle] = Pressure1_bar_1deg[:, cycle] - Avg_ManifoldOverlapPeriod_Pressure1[cycle] +  Intake_Manifold_pressure

Avg_overlapPeriod_Pressure1 = np.mean(Pressure1_bar_1deg[P1P2_open: P1P2_close, :], axis=0)
Avg_overlapPeriod_Pressure2 = np.mean(Pressure2_bar_1deg[P1P2_open: P1P2_close, :], axis=0)
# iterate through columns
for cycle in range(0, no_of_cycles):
    Pressure2_bar_pegged[:, cycle] = Pressure2_bar_1deg[:, cycle] - Avg_overlapPeriod_Pressure2[cycle] +  Avg_overlapPeriod_Pressure1[cycle]

# 5. COMBINING PRESSURE 1 and 2
# iterate through columns
for cycle in range(0, no_of_cycles):
    # iterate through rows
    for row in range(0, P1P2_middle):
        PressureCombined_bar[row,cycle] = Pressure1_bar_pegged[row, cycle]
    for row in range(P1P2_middle, 361):
        PressureCombined_bar[row,cycle] = Pressure2_bar_pegged[row, cycle]

# 6. VOLUME CALCULATION [ Pseudo code ]
l = 0.000100  # Connecting rod length
r = 0.000050  # Stroke length
b = 0.000050 # Bore
Vtdc = 0.000100 # Volume at TDC
RotorAngle = np.linspace(0, 360, 361)
Volume = np.zeros(361)
for angle in range(0, 361):
    cba = math.sqrt(l*l - r*math.sin(math.radians(angle))*r*math.sin(math.radians(angle)))
    Volume[angle] = Vtdc + 0.25*math.pi*b*b*(l + r - r*math.sin(math.radians(angle)) - cba)

# 7. PLOTTING
Avg_100cycle_Pressure1 = np.mean(Pressure1_bar_pegged, axis=1)
Avg_100cycle_Pressure2 = np.mean(Pressure2_bar_pegged, axis=1)
Avg_100cycle_PressureCombined = np.mean(PressureCombined_bar, axis=1)

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(RotorAngle, Avg_100cycle_Pressure1 )
axs[0, 0].set_title('Avg_100cycle_Pressure1 ')
axs[0, 0].set(xlabel='Rotor Angle [deg]', ylabel='Pressure [bar]')
axs[0, 1].plot(RotorAngle, Avg_100cycle_Pressure2, 'tab:orange')
axs[0, 1].set_title('Avg_100cycle_Pressure2 ')
axs[0, 1].set(xlabel='Rotor Angle [deg]', ylabel='Pressure [bar]')
axs[1, 0].plot(RotorAngle, Avg_100cycle_PressureCombined, 'tab:green')
axs[1, 0].set_title('Avg_100cycle_PressureCombined')
axs[1, 0].set(xlabel='Rotor Angle [deg]', ylabel='Pressure [bar]')
axs[1, 1].plot(Volume, PressureCombined_bar, 'tab:red')
axs[1, 1].set_title('P V')
axs[1, 1].set(xlabel='Volume [m^3]', ylabel='Pressure [bar]')

#for ax in axs.flat:
#    ax.set(xlabel='Rotor Angle [deg]', ylabel='Pressure [bar]')

plt.show()
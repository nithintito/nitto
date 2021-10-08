#https://forums.ni.com/t5/Multifunction-DAQ/Loop-timing-with-NIDAQmx-for-Python/td-p/3656140?profile.language=en
# https://documentation.help/NI-DAQmx/contWaveAcq.html
##############################################
# import libraries
import time as t
import numpy as np
import nidaqmx
import pprint
import csv
from collections import OrderedDict
from datetime import datetime

now = datetime.now() # current date and time

# filename
filename = 'C:/Users/ICElab/Desktop/Test1' + now.strftime("%d.%m.%Y") + '_' + now.strftime("%H_%M_%S") + '.csv'
#fieldnames = ["timeData", "Pressure1", "Pressure2"]
fieldnames =  OrderedDict([('timeData',None), ('EncoderA',None),('EncoderB',None), ('EncoderZ',None), ('Pressure1',None), ('Pressure2',None)])
with open(filename, 'wb', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
###############################################
# DAQ
fSampling = 2.0  # Hz
nSamples = 1  # samples
pp = pprint.PrettyPrinter(indent=4)
dtMax = 1  # sec

# config
with nidaqmx.Task() as task:
    t1 = t.time()
    task.ai_channels.add_ai_voltage_chan("Dev2/ai1:5")
    task.timing.cfg_samp_clk_timing(fSampling)

    t2 = t.time()
    dt = t2 - t1
    while dt < dtMax:
        data = task.read(number_of_samples_per_channel=nSamples)
        #EncoderA, EncoderB, EncoderZ, Pressure1, Pressure2 = task.read()
        t2 = t.time()
        dt = t2 - t1
        print (dt)
        pp.pprint(data)

        csv_writer.writerow({
            "timeData": dt,
            "Pressure1": data[0],
            "Pressure2": data[1],
            "EncoderA": data[2],
            "EncoderB": data[3],
            "EncoderZ": data[4]
        })

        # Logdata = {
        #     "timeData": dt,
        #     "Pressure1": Pressure1,
        #     "Pressure2": Pressure2,
        #     "EncoderA": EncoderA,
        #     "EncoderB": EncoderB,
        #     "EncoderZ": EncoderZ
        # }
        # csv_writer.writerow(Logdata)

###############################################
# output to file
#csv_writer.close()
# Terminate DAQ Device
#task.stop()
#task.close()

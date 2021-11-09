#https://forums.ni.com/t5/Multifunction-DAQ/Loop-timing-with-NIDAQmx-for-Python/td-p/3656140?profile.language=en
# https://github.com/ni/nidaqmx-python/blob/62fc6b48cbbb330fe1bcc9aedadc86610a1269b6/nidaqmx/error_codes.py
##############################################
# import libraries
from csv import writer
from csv import DictWriter
import time as t
import numpy as np
import nidaqmx
import pprint
from nidaqmx.constants import Edge, AcquisitionType
from nidaqmx.constants import FrequencyUnits

fSampling = 50000 # Hz
nSamples = 1#amples
pp = pprint.PrettyPrinter(indent=4)
dtMax = 2
###############################################
# DA
filename ='G:/Engine_DAQ_vi/EngineEdgeTrigger/teensy8.csv'
fieldnames = ["RotorAngle", "Pressure1", "Pressure2"]

field = ['RotorAngle',  'Pressure1', 'Pressure2']
with open(filename, 'w', newline='') as csv_file:
        csv_writer = DictWriter(csv_file, fieldnames=field)
        csv_writer.writeheader()

# config
c = 0
with nidaqmx.Task() as task:
    t1 = t.time()
    task.ai_channels.add_ai_voltage_chan("Dev2/ai1:2", min_val=-10, max_val=10)
    #task.ai_channels.add_ai_voltage_chan("Dev2/ai1", min_val=0, max_val=10)
    #task.timing.cfg_samp_clk_timing(fSampling, "/Dev2/PFI8", active_edge=Edge.RISING,
    #                                sample_mode=AcquisitionType.FINITE, samps_per_chan=1)
    task.timing.cfg_samp_clk_timing(fSampling, "/Dev2/PFI8", active_edge=Edge.RISING, sample_mode=AcquisitionType.CONTINUOUS)
    task.triggers.start_trigger.cfg_dig_edge_start_trig("/Dev2/PFI9", trigger_edge=Edge.RISING)

    #task.triggers.start_trigger.cfg_dig_edge_start_trig("/Dev2/PFI9", trigger_edge=Edge.RISING)
  #  task.timing.cfg_change_detection_timing(rising_edge_chan="/Dev2/PFI8", falling_edge_chan="/Dev2/PFI8", sample_mode=AcquisitionType.CONTINUOUS)
    angle=0
    t2 = t.time()
    dt = t2 - t1
    task.start()
    d0 = []
    d1 = []
    d2 = []
    d3 = []
    d4 = []
    m = 1
    while dt < dtMax:
        try:
            data = task.read(number_of_samples_per_channel=-1)
            #data = task.read(number_of_samples_per_channel=nSamples)
        except Exception as e:
            print(e)
            print(c)
        t2 = t.time()
        dt = t2 - t1
        d0.append(data[0][:])
        d1.append(data[1][:])
        #d2.append(data[2][:])
        #d3.append(data[3][:])
        #d4.append(data[4][:])
        #print (dt)
        #pp.pprint(data)
        c = c +1
        with open(filename, 'a', newline='') as csv_file:
            csv_writer = writer(csv_file)

            for i in range(0,len(data[0][:])):
                if (m==3):
                    angle = round(angle+0.34, 2)
                    m=0
                else:
                    angle = round(angle + 0.33, 2)
                m=m+1
                csv_writer.writerow([angle, float(data[0][i]), float(data[1][i])])
                                # float(data[2][i]), float(data[3][i]), float(data[4][i])])
    task.stop()
csv_file.close()
###############################################
# output to file
with nidaqmx.Task() as taskFreq:

    taskFreq.ci_channels.add_ci_freq_chan("Dev2/ctr0", min_val=1, max_val=500, units=FrequencyUnits.HZ)
    # Connect to ctr GATE channel for frequency measurement PFI 9
    # https://www.ni.com/pdf/manuals/371931f.pdf
    taskFreq.start()
    data = taskFreq.read()
    print(data)
    taskFreq.stop()
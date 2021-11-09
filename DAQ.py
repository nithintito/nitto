
"""
CLASS FOR DAQ
"""
import nidaqmx
from nidaqmx.constants import Edge,AcquisitionType,READ_ALL_AVAILABLE, TerminalConfiguration, FrequencyUnits
import nidaqmx.system
from configparser import ConfigParser
from CONFIGURE import CONFIG
import numpy as np

class DAQ(CONFIG):
       
    # Class Variable
     # 1. VARIABLES - File
    no_of_cycles_save = 10
     # 2. VARIABLES - Engine
    Rotor_Gear_Ratio = 3
     # 3. VARIABLES - DAQ
    DAQ_serial_no    = '1FB48FC'
    Pressure1_chanl  = 1      # Analog Input Channel pin no
    Pressure2_chanl  = 2      # Analog Input Channel pin no
    IntakePressure_chanl= 3   # Analog Input Channel pin no
    EncoderZ_chanl   = 4
    SamplingFreq     = 50000  # Hz ,  Sampling frequency = 250kHz / no of channels for NI 6210
    no_of_cycles_log = 100
    EncoderZ_Offset  = 0      # Angle after which the exact Rotor 0deg occurs after Encoder Z signal [ Always positive ]
    EncoderPPR       = 360    # Encoder pulse per revolution
    # 4.VARIABLES - Code
    Current_Cycle    = 1 
    Pressure1_log    = 0
    Pressure2_log    = 0
    IntakePressure_log = 0
    Speed_Hz_log     = 0
    RotorAngle       = 0
    n_rows           = 0
    
    # 1. The init method or constructor
    def __init__(self, filename = 'Default_configuration'):
           
        # Instance Variable
        CONFIG.__init__(self,filename)            
   
    # 2. Configure variables from DefaultConfiguration.ini file 
    def DAQ_VariableConfigure(self, filename = 'Default_configuration'):
        #configfile_Parsename =  's/C:/Users/ICElab/Desktop/RotoryEngineScan/data' + configfile_Parsename  + '.ini'
        configfilename   = CONFIG.CONFIG_ReturnConfigFile(self,filename)
        
        configfile_Parse = ConfigParser()
        configfile_Parse.read(configfilename)
        
        # VARIABLES CONFIGURE
                
        # 1. VARIABLES CONFIGURE - File
        self.no_of_cycles_save = configfile_Parse.getint('file','no_of_cycles_save')# No of cycle to be saved after post processing
        # 2. VARIABLES CONFIGURE - Engine
        self.Rotor_Gear_Ratio  = configfile_Parse.getint('engine','Rotor_Gear_Ratio')
        # 3. VARIABLES CONFIGURE - DAQ
        self.DAQ_serial_no     = configfile_Parse.get('daq','DAQ_serial_no')
        self.Pressure1_chanl   = configfile_Parse.getint('daq','Pressure1_chanl')  
        self.Pressure2_chanl   = configfile_Parse.getint('daq','Pressure2_chanl')  
        self.IntakePressure_chanl = configfile_Parse.getint('daq','IntakePressure_chanl')
        self.EncoderZ_chanl   = configfile_Parse.getint('daq','EncoderZ_chanl')
        self.SamplingFreq     = configfile_Parse.getint('daq','SamplingFreq')          # Hz ,  Sampling frequency = 250kHz / no of channels for NI 6210
        self.no_of_cycles_log = configfile_Parse.getint('daq','no_of_cycles_log')
        self.EncoderZ_Offset  = configfile_Parse.getint('daq','EncoderZ_Offset')      # Angle after which the exact Rotor 0deg occurs after Encoder Z signal [ Always positive ]
        self.EncoderPPR       = configfile_Parse.getint('daq','EncoderPPR' )
        # 4.VARIABLES CONFIGURE - Code
        self.Current_Cycle = 1  
        self.nrows         = int (self.EncoderPPR * self.Rotor_Gear_Ratio  )  # 360x 3 
        self.Pressure1_log = np.zeros([self.nrows, self.no_of_cycles_log],dtype = float)
        self.Pressure2_log = np.zeros([self.nrows, self.no_of_cycles_log],dtype = float)
        self.IntakePressure_log = np.zeros([self.nrows, self.no_of_cycles_log],dtype = float)
        self.Speed_Hz_log  = np.zeros([self.nrows, self.no_of_cycles_log],dtype = float)
        self.RotorAngle = np.linspace(0, 360, self.nrows)[np.newaxis]
        #RotorAngle = np.linspace(0, 360, 1080)[np.newaxis]
        self.RotorAngle = np.round(self.RotorAngle.T, 1)
        
            no of sensors = 4
                1080 x no of cycles 
                
             3D matrix  =    no of sensors x 1080 x no of cycles
             
             Status
             
             data frame or 3D matrix
             
             Data ready .copy
             
             updated
             
             
     
     # 3. Configure DAQ from DefaultConfiguration.ini file 
    def DAQ_HardwareConfigure(self):
       system = nidaqmx.system.System.local()
        
       for device in system.devices: # Searching for hardware with same serial no [ License check ]
            if ( device.product_num == self.DAQ_serial_no) :
            #print('Device Name: {0}, Product Category: {1}, Product Type: {2}', Serial Number: {3}'.format(
             #   device.name, device.product_category, device.product_type, device.product_num))
                             
                return True
            else:
               #print (" Device Not Connected ")
               return False
           
#               global Acquisition_Start_Stop # Needed to modify global copy of this variable
#               Acquisition_Start_Stop = False
#               self.User_Start_Stop()
               # @@@@@@@@@@@@@@ Try better logic like "wait" than calling STOP ACQUISITION , current implementation will reset the configuration file and go in loop back here
               
    # 4. LOGGING DATA FRM DAQ  [ THREAD ]
    def DAQ_Log(self):    
        if (DAQ_Status == True)
        # Starting the nidaqmx task 
        Analog_PressureRead_task.ai_channels.add_ai_voltage_chan(device.ai_physical_chans[self.Pressure1_chanl].name,
                                                                 min_val=-10, max_val=10,
                                                                 terminal_config=TerminalConfiguration.DIFFERENTIAL)
        Analog_PressureRead_task.ai_channels.add_ai_voltage_chan(device.ai_physical_chans[self.Pressure2_chanl].name,
                                                                 min_val=-10, max_val=10,
                                                                 terminal_config=TerminalConfiguration.DIFFERENTIAL)
        Analog_PressureRead_task.ai_channels.add_ai_voltage_chan(device.ai_physical_chans[self.IntakePressure_chanl].name,
                                                                 min_val=-10, max_val=10,
                                                                 terminal_config=TerminalConfiguration.DIFFERENTIAL)
        Analog_PressureRead_task.ai_channels.add_ai_voltage_chan(device.ai_physical_chans[self.EncoderZ_chanl].name,
                                                                 min_val=-10, max_val=10,
                                                                 terminal_config=TerminalConfiguration.DIFFERENTIAL)
        #@@@@@@@@@@@@@@@@@@@@@@@@@ Change to dynamic device name @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        Analog_PressureRead_task.timing.cfg_samp_clk_timing(self.SamplingFreq, "/Dev2/PFI8", active_edge=Edge.RISING,
                                                            sample_mode=AcquisitionType.CONTINUOUS)
        Analog_PressureRead_task.triggers.start_trigger.cfg_dig_edge_start_trig("/Dev2/PFI9", trigger_edge=Edge.RISING)
        
        Counter_FrequencyRead_task.ci_channels.add_ci_freq_chan("Dev2/ctr0", min_val=1, max_val=500,
                                                                units=FrequencyUnits.HZ)
       # Connect to ctr GATE channel for frequency measurement PFI 9
       # https://www.ni.com/pdf/manuals/371931f.pdf
       Counter_FrequencyRead_task.start()
       Analog_PressureRead_task.start()
        
        #n_rows         = int (self.EncoderPPR * self.Rotor_Gear_Ratio  )  # 360x 3 
        angle_counter = 0
        while angle_counter < self.EncoderZ_Offset:    # Dont log till 0 angle, reading the data out of buffer
            try:
                data = Analog_PressureRead_task.read(number_of_samples_per_channel=1)  # Read only one sample
                Freq_data = Counter_FrequencyRead_task.read()
            except Exception as e:
                print(e)
                print(angle_counter,"\n")
                angle_counter = angle_counter + 1
                angle_counter = angle_counter - self.EncoderZ_Offset
                print(angle_counter, "\n START LOGGING")
        m = 1
        while angle_counter < self.n_rows:    # cyclex360x3 = 108000
            try:
                data = Analog_PressureRead_task.read(number_of_samples_per_channel=-1) # READ_ALL_AVAILABLE
                Freq_data = Counter_FrequencyRead_task.read()
            except Exception as e:
                print(e)
                print(angle_counter)

            m = angle_counter + len(data[0][:])
            if (m<self.n_rows):
                data_final[angle_counter:m, 2] = data[0][:]  # Pressure 1
                data_final[angle_counter:m, 3] = data[1][:]  # Pressure 2
                data_final[angle_counter:m, 4] = data[2][:]  # IntakePressure
                data_final[angle_counter:m, 5] = data[3][:]  # Encoder Z voltage
                data_final[angle_counter:m, 6] = Freq_data   # Encoder Z frequency
            else:
                data_final[angle_counter:self.n_rows, 2] = data[0][:self.n_rows - angle_counter]  # Pressure 1
                data_final[angle_counter:self.n_rows, 3] = data[1][:self.n_rows - angle_counter]  # Pressure 2
                data_final[angle_counter:self.n_rows, 4] = data[2][:self.n_rows - angle_counter]  # IntakePressure
                data_final[angle_counter:self.n_rows, 5] = data[3][:self.n_rows - angle_counter]  # Encoder Z voltage
                data_final[angle_counter:self.n_rows, 6] = Freq_data                         # Encoder Z frequency
        angle_counter = m
           
    # 5. Sending data to Post Processing
    def DAQ_DataForPostProcess(self, cycle):
        return Pressure1
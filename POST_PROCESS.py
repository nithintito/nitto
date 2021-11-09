# -*- coding: utf-8 -*-
from configparser import ConfigParser
from CONFIGURE import CONFIG
import numpy as np

class POST_PROCESS(CONFIG):
       
    # Class Variable
     # 1. VARIABLES - File
    save_folder = None        # Folder to save final data
    filename1 = None          # MSP - Manifold Steam Pressure
    filename2 = None          # RPM 
    filename3 = None          # Nm
    no_of_cycles_save = 10    # No of cycle to be saved after post processing
    
    # 2. VARIABLES - Engine
    Intake_Manifold_Open_Angle  = 10
    Intake_Manifold_Close_Angle = 30
    P1_Open_Angle  = 5
    P1_Close_Angle = 130 
    P2_Open_Angle  = 125
    P2_Close_Angle = 195
    Incylinder_Pressure_Calibration_Mulitplier = 10
    Incylinder_Pressure_Calibration_Offset     = 0
    Intake_Manifold_Pressure_Calibration_Mulitplier = 10
    Intake_Manifold_Pressure_Calibration_Offset     = 0
    Rotor_Gear_Ratio = 3
     # 3. VARIABLES - DAQ
    EncoderPPR       = 360    # Encoder pulse per revolution
     # 4.VARIABLES - Code
    Intake_Manifold_Open_Index   = 0 # _Index   = 3x _Angle  ie Row index of corresponding angle
    Intake_Manifold_Close_Index  = 0
    P1_Open_Index                = 0
    P1_Close_Index               = 0
    P2_Open_Index                = 0
    P2_Close_Index               = 0
    Pressure1_bar_peg            = 0
    Pressure2_bar_peg            = 0
    IntakePressure_bar_peg       = 0
    Speed_rpm                    = 0
    RotorAngle                   = 0
    
    # The init method or constructor
    def __init__(self, filename = 'Default_configuration'):
           
        # Instance Variable
        CONFIG.__init__(self,filename)            
   
    # Configure variables from DefaultConfiguration.ini file 
    def POST_PROCESS_Configure(self, filename = 'Default_configuration'):
        #config_filename =  's/C:/Users/ICElab/Desktop/RotoryEngineScan/data' + config_filename  + '.ini'
        configfilename = CONFIG.CONFIG_ReturnConfigFile(self,filename)
        
        configfile_Parse = ConfigParser()
        configfile_Parse.read(configfilename)
        
        # VARIABLES CONFIGURE
                
        # 1. VARIABLES CONFIGURE - File
        no_of_cycles_save  = configfile_Parse.getint('file','no_of_cycles_save')# No of cycle to be saved after post processing
        save_folder  = configfile_Parse.get('file','save_folder')      # Folder to save final data
        filename1    = configfile_Parse.get('file','filename1')       # MSP - Manifold Steam Pressure
        filename2    = configfile_Parse.get('file','filename2')      # RPM 
        filename3    = configfile_Parse.get('file','filename3')      # Nm
        
        # 2. VARIABLES CONFIGURE - Engine
        Intake_Manifold_Open_Angle  = configfile_Parse.getint('engine','Intake_Manifold_Open_Angle')
        Intake_Manifold_Close_Angle = configfile_Parse.getint('engine','Intake_Manifold_Close_Angle')
        P1_Open_Angle     = configfile_Parse.getint('engine','P1_Open_Angle')
        P1_Close_Angle    = configfile_Parse.getint('engine','P1_Close_Angle')
        P2_Open_Angle     = configfile_Parse.getint('engine','P2_Open_Angle')
        P2_Close_Angle    = configfile_Parse.getint('engine','P2_Close_Angle')
        Incylinder_Pressure_Calibration_Mulitplier = configfile_Parse.getfloat('engine','Incylinder_Pressure_Calibration_Mulitplier')
        Incylinder_Pressure_Calibration_Offset     = configfile_Parse.getfloat('engine','Incylinder_Pressure_Calibration_Offset')
        Intake_Manifold_Pressure_Calibration_Mulitplier = configfile_Parse.getfloat('engine','Intake_Manifold_Pressure_Calibration_Mulitplier')
        Intake_Manifold_Pressure_Calibration_Offset     = configfile_Parse.getfloat('engine','Intake_Manifold_Pressure_Calibration_Offset')
        Rotor_Gear_Ratio  = configfile_Parse.getint('engine','Rotor_Gear_Ratio')
        # 3. VARIABLES CONFIGURE- DAQ
        EncoderPPR       = configfile_Parse.getint('daq','EncoderPPR' )
        # 4.VARIABLES - Code
        Intake_Manifold_Open_Index = int (Intake_Manifold_Open_Angle * Rotor_Gear_Ratio )   # _Index   = 3x _Angle  ie Row index of corresponding angle
        Intake_Manifold_Close_Index = int (Intake_Manifold_Close_Angle * Rotor_Gear_Ratio )
        P1_Open_Index  = int ( P1_Open_Index * Rotor_Gear_Ratio )
        P1_Close_Index = int ( P1_Close_Index * Rotor_Gear_Ratio )
        P2_Open_Index  = int ( P2_Open_Index * Rotor_Gear_Ratio )
        P2_Close_Index = int ( P2_Close_Index * Rotor_Gear_Ratio )
        nrows = int (EncoderPPR * Rotor_Gear_Ratio  )  # 360x 3 
        Pressure1_bar_peg = np.zeros([nrows, no_of_cycles_save],dtype = float)  # We process for no_of_cycles_save ( eg : 10 ) out of no_of_cycles_log ( eg : 100 ) 
        Pressure2_bar_peg = np.zeros([nrows, no_of_cycles_save],dtype = float)
        IntakePressure_bar_peg = np.zeros([1, no_of_cycles_save],dtype = float) # We average Intake Manifold Press for each cycle
        Speed_rpm = np.zeros([1, no_of_cycles_save],dtype = float)
        
        RotorAngle = np.linspace(0, 360, EncoderPPR* Rotor_Gear_Ratio)[np.newaxis]
        #RotorAngle = np.linspace(0, 360, 1080)[np.newaxis]
        RotorAngle = np.round(RotorAngle.T, 1)
        
    # Retrieves instance variable    
    def POST_PROCESS_Calculate(self):    
        return self.color  
    
    # 2. SAVE PROCESSED FILE ON PRESSING "SAVE" BUTTON IN GUI    
    def POST_PROCESS_Save(self, filename = 'Default_configuration',filname1= None, filname2= None, filname3= None):    
        #config_filename =  's/C:/Users/ICElab/Desktop/RotoryEngineScan/data' + config_filename  + '.ini'
        configfilename = CONFIG.CONFIG_ReturnConfigFile(self,filename)
        
        configfile_Parse = ConfigParser()
        configfile_Parse.read(configfilename)
                
        #save_folder  = configfile_Parse.get('file','save_folder')      # Folder to save final data
        filename1    = filname1       # MSP - Manifold Steam Pressure
        filename2    = filname2      # RPM 
        filename3    = filname3      # Nm
        now = datetime.datetime.now()
        # filename
        savefile  = save_folder + now.strftime("%d.%m.%Y") + '_' + now.strftime("%H.%M.%S") + '_' + filename1 + filename2 + filename3 + '.csv'
        #LoggedData = pd.DataFrame(columns=['RotorAngle',  'cycle ' ,'Pressure1', 'Pressure2',' IntakePressure',' EncoderZfreq'])
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  CORRECT BELOW LNES @@@@@@@@@
        np.savetxt(savefile, data_final, delimiter=',', header="RotorAngle, Pressure1, Pressure2, IntakePressure , EncoderZfreq")
        if savefile.write:
            return True
        else:
            return False
    
    # Retrieves instance variable    
    def POST_PROCESS_DataForPlot(self):    
        return self.P  
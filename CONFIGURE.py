"""
CLASS FOR CONFIGURATION .ini FILE 
"""
from configparser import ConfigParser

class CONFIG:
       
    # Class Variable
    Config_folder   = r'C:\Users\TITO\Desktop\RotoryEngineScan\data' 
    Config_filename = 'Default_configuration'
    Config_file     = None    
       
    # The init method or constructor
    def __init__(self, filename = 'Default_configuration'):
           
        # Instance Variable
        self.Config_folder   = r'C:\Users\ICElab\Desktop\RotoryEngineScan\data'    
        self.Config_filename =  filename       
        self.Config_file     = self.Config_folder + '\\' + self.Config_filename + '.ini'
    
    # Returns active config file path
    def CONFIG_ReturnConfigFile(self, filename = 'Default_configuration'):
        self.Config_folder   = r'C:\Users\ICElab\Desktop\RotoryEngineScan\data'    
        self.Config_filename =  filename       
        self.Config_file     = self.Config_folder +  '\\' + self.Config_filename + '.ini'
        return self.Config_file
       
    #@@@@@@@@@@@@@ [ ADD SAVE CONFIGURE FILE LATER]@@@@@@@@@@@@@@   
    def CONFIG_SaveConfigFile(self, filename = 'Default_configuration'):    
        self.Config_file     = self.Config_folder +  '\\' + self.Config_filename + '.ini'
        #@@@@@@@@@@@@@@@@@@@  Save .ini file @@@@@@@@@@@@@
        config = ConfigParser()
        
        config['file']['save_folder'] = r'C:\Users\ICElab\Desktop\RotoryEngineScan\data'  # update
        config['file']['filename1']   = 'Nm'   
        
        with open(self.Config_file, 'w') as configfile:    # save
            config.write(configfile)

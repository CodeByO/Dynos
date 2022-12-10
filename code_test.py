import unittest
import os
from pyinjector import inject
import psutil


import Dynos
import warnings
import subprocess
from uac_bypass import uac_bypass
'''
테스트 목록
1. Listdlls가 정상 동작하는지

2. cmake가 존재 하는지

3. strings 명령어가 정상 동작하는지

4. Register UAC Bypass가 정상 동작하는지

5. pyinjector가 정상동작 하는지
'''
def create_process(path):
    return subprocess.Popen([path]).pid

def list_dll(pid):
    
        list_dll_path = os.getcwd() + "/" + "Listdlls.exe "
        list_dll_path = list_dll_path.replace("\\","/")
        stream = os.popen(list_dll_path + str(pid))
        
        dlls = stream.read()
        program_name = ""
        list_dlls = []
        list_programs = []
        path_lists = []

        try:
            split_text = dlls.replace("\\","/").replace('  ','\n').split('\n')
            
       
            for i in split_text:
                path_lists.append(i.replace(" ",""))
            
            for i in path_lists:
                if i.endswith(".exe"):
                    list_programs.append(i)
                if i.endswith(".dll"):
                    list_dlls.append(i)   
            for i in list_programs:
                if i.startswith("C:/"):
                    program_name = i
        except:
            print("\nERROR::rWrong pid...")
        return program_name, list_dlls
class DynosTest(unittest.TestCase):


    def setUp(self):
        warnings.filterwarnings(action='ignore')
        
        self.uac_bypass = uac_bypass()
        self.mainDll_path = os.getcwd() + "/ExamDLL2/CreateDLL/x64/Debug/MainDLL.exe"
        self.mainDll_path = self.mainDll_path.replace("\\","/")
          
    def test_cmake(self):
        stream = os.popen("cmake")
        cmake = stream.read()
        self.assertTrue(cmake.startswith("Usage"))
    
    def test_listdll(self):
        pid = create_process(self.mainDll_path)
        
        programName, self.list_dlls = list_dll(pid)
        self.assertIsInstance(programName,str)
        self.assertIsInstance(self.list_dlls,list)
        
        psutil.Process(pid).kill()   

    def test_strings(self):
        strings = "strings " + self.mainDll_path
        stream = os.popen(strings)
        
        string = stream.read()
        
        self.assertTrue(string.startswith("!This program cannot be run in DOS mode."))
    
    def test_uac_bypass(self):
        pid = self.uac_bypass.execute()
        
        self.assertIsInstance(pid,int)
        psutil.Process(pid).kill()  

    def test_injection(self):
        pid = create_process(self.mainDll_path)
        dll_path = os.getcwd() + "/test.dll"
        self.assertIsInstance(inject(pid,dll_path),int)
        
        psutil.Process(pid).kill()

if __name__ == '__main__':
    unittest.main()
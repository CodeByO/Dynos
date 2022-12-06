import unittest
import os
from pyinjector import inject
import psutil
from pywinauto.application import Application
import pywinauto
import time
import subprocess
import Dynos
import warnings
'''
테스트 목록
1. Listdlls가 정상 동작하는지

2. cmake가 존재 하는지

3. strings 명령어가 정상 동작하는지

4. Register UAC Bypass가 정상 동작하는지

5. pyinjector가 정상동작 하는지
'''

class DynosTest(unittest.TestCase):


    def setUp(self):
        warnings.filterwarnings(action='ignore')

        self.hijack = Dynos.hiJacking()
        self.inject = Dynos.injection()
        self.uac_bypass = Dynos.uac_bypass()
        
        self.mainDll_path = os.getcwd() + "/ExamDLL2/CreateDLL/x64/Debug/MainDLL.exe"
        self.mainDll_path = self.mainDll_path.replace("\\","/")
          
    def test_cmake(self):
        stream = os.popen("cmake")
        cmake = stream.read()
        self.assertTrue(cmake.startswith("Usage"))
    
    def test_listdll(self):
        pid = self.hijack.create_process(self.mainDll_path)
        
        programName, self.list_dlls = self.hijack.list_dll(pid)
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
        pid = self.hijack.create_process(self.mainDll_path)
        dll_path = os.getcwd() + "/test.dll"
        self.assertIsInstance(inject(pid,dll_path),int)
        
        psutil.Process(pid).kill()

if __name__ == '__main__':
    unittest.main()
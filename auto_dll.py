import os
import time
from tqdm import tqdm
from pyinjector import inject
import subprocess
def list_dll(pid):
    stream = os.popen("Listdlls.exe " + str(pid))
    dlls = stream.read()
    program_name = ""
    try:
        program_name = dlls.split("\n")[7]
        program_name = program_name.replace("Command line: ", '').replace('"', '').replace(' -bystartup','').replace('\\','/')
    except:
        print("Wrong pid...")
    
    
    if 'C:/' not in program_name:
        name_split = program_name.split('/')
        name = name_split[-1]
        for dirpath, dirname, filename in tqdm(os.walk("C:/Users/codeb/Desktop/ExamDLL")):
            if name in filename:
                program_name =  os.path.join(dirpath, name)

    split_text = dlls.replace("\\","/").replace(' ', '\n').split('\n')
    list_dlls = []
    for i in split_text:
        if i.endswith(".dll"):
            
            list_dlls.append(i)
    return program_name, list_dlls
    
    #endswith(dll)
def check_permission(path):
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

def find_string(name,list_name,list_dir):
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
    
def create_process(path):
        return subprocess.Popen([path]).pid

if __name__=='__main__':
    path_exe = "C:/Users/codeb/Desktop/ExamDLL2/CreateDLL/x64/Debug/MainDLL.exe"
    path_dll = "C:/Users/codeb/Desktop/CreateDLL.dll"
    pid = create_process(path_exe)
    
    program_name, list_dlls = list_dll(pid)
    file_list,dir_list = check_permission(list_dlls)
    if not len(file_list) == 0:
        if find_string(program_name,file_list,dir_list):
            print("Detect programs vulnerable to dll injection")
            inject(pid,path_dll)
        else:
            print("Nah....")
    else:
        print("Not Found writable dir")
    
        
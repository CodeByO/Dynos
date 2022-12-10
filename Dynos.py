from pywinauto import *
from injection import injection
from hijacking import hiJacking


                        
               
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
        
        

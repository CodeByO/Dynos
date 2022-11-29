#include <windows.h>
#include <iostream>
#include "shobjidl.h"
using namespace std;

HRESULT CopyItem(__in PCWSTR pszSrcItem, __in PCWSTR pszDest, PCWSTR pszNewName)
{
    //
    // Initialize COM as STA.
    //
    HRESULT hr = CoInitializeEx(NULL, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE); 
    if (SUCCEEDED(hr))
    {
        IFileOperation *pfo;
  
        //
        // Create the IFileOperation interface 
        //
        hr = CoCreateInstance(CLSID_FileOperation, 
                              NULL, 
                              CLSCTX_ALL, 
                              IID_PPV_ARGS(&pfo));
        if (SUCCEEDED(hr))
        {
            //
            // Set the operation flags. Turn off all UI from being shown to the
            // user during the operation. This includes error, confirmation,
            // and progress dialogs.
            //
            hr = pfo->SetOperationFlags(FOF_NOCONFIRMATION);
            if (SUCCEEDED(hr))
            {
                //
                // Create an IShellItem from the supplied source path.
                //
                IShellItem *psiFrom = NULL;
                hr = SHCreateItemFromParsingName(pszSrcItem, 
                                                 NULL, 
                                                 IID_PPV_ARGS(&psiFrom));
                if (SUCCEEDED(hr))
                {
                    IShellItem *psiTo = NULL;
  
                    if (NULL != pszDest)
                    {
                        //
                        // Create an IShellItem from the supplied 
                        // destination path.
                        //
                        hr = SHCreateItemFromParsingName(pszDest, 
                                                         NULL, 
                                                         IID_PPV_ARGS(&psiTo));
                    }
                    
                    if (SUCCEEDED(hr))
                    {
                        //
                        // Add the operation
                        //
                        hr = pfo->CopyItem(psiFrom, psiTo, pszNewName, NULL);

                        if (NULL != psiTo)
                        {
                            psiTo->Release();
                        }
                    }
                    
                    psiFrom->Release();
                }
                
                if (SUCCEEDED(hr))
                {
                    //
                    // Perform the operation to copy the file.
                    //
                    hr = pfo->PerformOperations();
                }        
            }
            
            //
            // Release the IFileOperation interface.
            //
            pfo->Release();
        }
  
        CoUninitialize();
    }
    return hr;
}

bool __stdcall DllMain(HMODULE /*module*/, DWORD reason, LPVOID /*reserved*/) {
    
    PCWSTR srcPath = L"C:\\Users\\codeb\\Desktop\\test.txt";
    PCWSTR desPath = L"C:\\Users\\codeb\\Desktop\\test\\";
    PCWSTR FileName = L"hack.txt";
    HRESULT res2;
    if (reason == DLL_PROCESS_ATTACH){
        res2 = CopyItem(srcPath, desPath, FileName);
        AllocConsole();
        FILE* fp = freopen("CONOUT$", "w", stdout);
        //cout << res << endl;
        cout << res2 << endl;
        return true;
    }
    if(reason == DLL_THREAD_ATTACH){
        res2 = CopyItem(srcPath, desPath, FileName);
        AllocConsole();
        FILE* fp = freopen("CONOUT$", "w", stdout);
        cout << res2 << endl;
        return true;
    }
    
    
}
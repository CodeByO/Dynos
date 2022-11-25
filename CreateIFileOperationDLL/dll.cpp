#include <windows.h>
#include <iostream>
#include <shobjidl.h>

using namespace std;

void hello() {
    AllocConsole();
    freopen("CONOUT$", "w", stdout);
    cout << "Hello, World!" << endl;
}

bool __stdcall DllMain(HMODULE /*module*/, DWORD reason, LPVOID /*reserved*/) {
    if (reason == DLL_PROCESS_ATTACH) hello();
    return true;
}
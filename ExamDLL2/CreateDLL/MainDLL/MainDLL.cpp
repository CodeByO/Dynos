// MainDLL.cpp : 이 파일에는 'main' 함수가 포함됩니다. 거기서 프로그램 실행이 시작되고 종료됩니다.
//

#include <Windows.h>
#include <iostream>
#include <stdlib.h>
//#include "../CreateDLL/MyMath.h"

typedef double (*DLL_SUM)(double a, double b);

int main()
{
	std::string path = "CreateDLL.dll";

	HMODULE hDll = ::LoadLibraryA(path.c_str()); Sleep(1000);
	if (hDll != NULL)
	{
		DLL_SUM pFunc = (DLL_SUM)::GetProcAddress(hDll, "Sum");
		double ret = pFunc(5.0, 7.0);
		std::cout << "Result: " << ret << std::endl;

		::FreeLibrary(hDll);
		system("pause");
	}
	else {
		std::cout << "Fail!" << std::endl;
	}

}


#pragma once

#define WIN32_LEAN_AND_MEAN             // 거의 사용되지 않는 내용을 Windows 헤더에서 제외합니다.
// Windows 헤더 파일
#include <windows.h>
#include <iostream>
#include <objbase.h>
#include <ShobjIdl.h>
#include <shobjidl_core.h>
#include <Shellapi.h>     // Included for shell constants such as FO_* values
#include <shlobj.h>       // Required for necessary shell dependencies
#include <strsafe.h> 
#include <string>
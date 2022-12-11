# Dynos

Dynos(Dynamic Link Library + Tanos)

DLL auto Injection and Hijacking tool 

## 프로젝트 목적

이 프로젝트는 DLL 관련 취약점인 DLL Hijacking 과 DLL Injection 공격을 자동화 하여 DLL 취약점을 찾게 해주는 것이 목표 입니다.


## 제공하는 기능

Dynos는 Hijacking + Injection을 합쳐서 총 4개의 기능을 제공 합니다.



## Hijacking

 1. Normal Hijacking

    이 공격은 기본적인 DLL 취약점을 검증합니다.
    '''
     
     조건

        LoadLibrary를 호출할 때, DLL 경로를 하드 코딩 또는 DLL 이름을 넣은 경우(명시적 로딩일 경우)

        로드하는 DLL 경로가 일반 사용자도 쓰기 권한이 있는 경우


    '''

2. Search Order Hijacking

    이 공격은 DLL Search Order를 악용하여 취약점을 검증합니다.

    '''
    조건

        LoadLibrary를 호출할 때, DLL 인자를 절대 경로가 아닌 파일 이름으로 넣어 DLL Search Order가 실행 될때

    '''


3. Abusing IFileOperation

    이 공격은 Microsoft 서명이 있는 프로세스에서 IFileOperation을 사용하면 자동으로 권한 상승이 되는 점을 악용하여 취약점을 검증합니다.

    '''
    조건

        cmake가 설치 및 환경 변수로 등록되어 있을 때

        *주의*

            현재 이 공격은 완벽하게 동작하지 않습니다.

            공격을 수행해보고 싶으면 관리자 권한이 있는 powershell에 수행하는 것을 추천드립니다.

    '''
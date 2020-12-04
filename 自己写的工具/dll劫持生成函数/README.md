## DLL函数生成 ##
根据config.json配置对应要生成的函数类型、函数名称、参数类型、参数数量
```json
{
  "functions": [
    {"type": "void", "name": "wdCommandDispatch","arg":{"type":"","number":0}},
    {"type": "void","name": "wdGetApplicationObject","arg":{"type":"","number":0}},
    {"type": "int", "name": "FMain","arg":{"type":"int","number":4}}
  ]
}
```

![](img/create.png)

生成结果示例
```c
#include "stdafx.h"
#include <iostream>
#include <Windows.h>

extern "C" __declspec(dllexport) void wdCommandDispatch();
extern "C" __declspec(dllexport) void wdGetApplicationObject();
extern "C" __declspec(dllexport) int FMain(int a,int b,int c,int d);

void wdCommandDispatch(){

}

void wdGetApplicationObject(){

}

int FMain(int a,int b,int c,int d){

}



BOOL APIENTRY DllMain(
	HINSTANCE hinstDLL,  // handle to DLL module
	DWORD fdwReason,     // reason for calling function
	LPVOID lpReserved)  // reserved
{
	// Perform actions based on the reason for calling.
	switch (fdwReason)
	{
	case DLL_PROCESS_ATTACH:
		// Initialize once for each new process.
		// Return FALSE to fail DLL load.
		break;

	case DLL_THREAD_ATTACH:
		// Do thread-specific initialization.
		break;

	case DLL_THREAD_DETACH:
		// Do thread-specific cleanup.
		break;

	case DLL_PROCESS_DETACH:
		// Perform any necessary cleanup.
		break;
	}
	return TRUE;  // Successful DLL_PROCESS_ATTACH.
}
        

```
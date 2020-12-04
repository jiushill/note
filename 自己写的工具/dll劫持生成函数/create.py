import json

class CreateFunction(object):
    def __init__(self):
        self.config = json.loads(open(r"config.json", "r").read())
        self.data='''#include "stdafx.h"
#include <iostream>
#include <Windows.h>

{function}
{function2}
'''

        self.data2='''
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
        '''

    def create(self):
        data=""
        data2=""
        functions=self.config['functions']
        for f in functions:
            if int(f['arg']['number'])>0:
                args=""
                number=int(f['arg']['number'])
                types=f['arg']['type']
                for a in range(97,97+number):
                    args+="{} {},".format(types,chr(a))
                args=args.rstrip(",")
            else:
                args=""
            data+='extern "C" __declspec(dllexport) {} {}({});\n'.format(f['type'],f['name'],args)
            data2+=f['type']+' {}'.format(f['name'])+'({})'.format(args)+'{\n'+'\n}\n\n'

        print(self.data.format(function=data,function2=data2)+self.data2,file=open("functions.c","a",encoding="utf-8"))
        print("[<+>] create functions file,Sucess->functions.c")

if __name__ == '__main__':
    obj=CreateFunction()
    obj.create()

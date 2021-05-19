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

## DLL代理转发生成 ##
```text
python create2.py -f C:\Windows\System32\kernel32.dll
kernel32
#pragma comment(linker,"/export:AcquireSRWLockExclusive=kernel32.AcquireSRWLockExclusive,@1")
#pragma comment(linker,"/export:AcquireSRWLockShared=kernel32.AcquireSRWLockShared,@2")
#pragma comment(linker,"/export:ActivateActCtx=kernel32.ActivateActCtx,@3")
#pragma comment(linker,"/export:ActivateActCtxWorker=kernel32.ActivateActCtxWorker,@4")
#pragma comment(linker,"/export:AddAtomA=kernel32.AddAtomA,@5")
#pragma comment(linker,"/export:AddAtomW=kernel32.AddAtomW,@6")
#pragma comment(linker,"/export:AddConsoleAliasA=kernel32.AddConsoleAliasA,@7")
#pragma comment(linker,"/export:AddConsoleAliasW=kernel32.AddConsoleAliasW,@8")
#pragma comment(linker,"/export:AddDllDirectory=kernel32.AddDllDirectory,@9")
#pragma comment(linker,"/export:AddIntegrityLabelToBoundaryDescriptor=kernel32.AddIntegrityLabelToBoundaryDescriptor,@10")
#pragma comment(linker,"/export:AddLocalAlternateComputerNameA=kernel32.AddLocalAlternateComputerNameA,@11")
#pragma comment(linker,"/export:AddLocalAlternateComputerNameW=kernel32.AddLocalAlternateComputerNameW,@12")
#pragma comment(linker,"/export:AddRefActCtx=kernel32.AddRefActCtx,@13")
#pragma comment(linker,"/export:AddRefActCtxWorker=kernel32.AddRefActCtxWorker,@14")
#pragma comment(linker,"/export:AddResourceAttributeAce=kernel32.AddResourceAttributeAce,@15")
#pragma comment(linker,"/export:AddSIDToBoundaryDescriptor=kernel32.AddSIDToBoundaryDescriptor,@16")
#pragma comment(linker,"/export:AddScopedPolicyIDAce=kernel32.AddScopedPolicyIDAce,@17")
#pragma comment(linker,"/export:AddSecureMemoryCacheCallback=kernel32.AddSecureMemoryCacheCallback,@18")
#pragma comment(linker,"/export:AddVectoredContinueHandler=kernel32.AddVectoredContinueHandler,@19")
#pragma comment(linker,"/export:AddVectoredExceptionHandler=kernel32.AddVectoredExceptionHandler,@20")
#pragma comment(linker,"/export:AdjustCalendarDate=kernel32.AdjustCalendarDate,@21")
#pragma comment(linker,"/export:AllocConsole=kernel32.AllocConsole,@22")
#pragma comment(linker,"/export:AllocateUserPhysicalPages=kernel32.AllocateUserPhysicalPages,@23")
#pragma comment(linker,"/export:AllocateUserPhysicalPagesNuma=kernel32.AllocateUserPhysicalPagesNuma,@24")
#pragma comment(linker,"/export:AppPolicyGetClrCompat=kernel32.AppPolicyGetClrCompat,@25")
#pragma comment(linker,"/export:AppPolicyGetCreateFileAccess=kernel32.AppPolicyGetCreateFileAccess,@26")
#pragma comment(linker,"/export:AppPolicyGetLifecycleManagement=kernel32.AppPolicyGetLifecycleManagement,@27")
#pragma comment(linker,"/export:AppPolicyGetMediaFoundationCodecLoading=kernel32.AppPolicyGetMediaFoundationCodecLoading,@28")
#pragma comment(linker,"/export:AppPolicyGetProcessTerminationMethod=kernel32.AppPolicyGetProcessTerminationMethod,@29")
#pragma comment(linker,"/export:AppPolicyGetShowDeveloperDiagnostic=kernel32.AppPolicyGetShowDeveloperDiagnostic,@30")
#pragma comment(linker,"/export:AppPolicyGetThreadInitializationType=kernel32.AppPolicyGetThreadInitializationType,@31")
#pragma comment(linker,"/export:AppPolicyGetWindowingModel=kernel32.AppPolicyGetWindowingModel,@32")
#pragma comment(linker,"/export:AppXGetOSMaxVersionTested=kernel32.AppXGetOSMaxVersionTested,@33")
#pragma comment(linker,"/export:ApplicationRecoveryFinished=kernel32.ApplicationRecoveryFinished,@34")
#pragma comment(linker,"/export:ApplicationRecoveryInProgress=kernel32.ApplicationRecoveryInProgress,@35")
#pragma comment(linker,"/export:AreFileApisANSI=kernel32.AreFileApisANSI,@36")
#pragma comment(linker,"/export:AssignProcessToJobObject=kernel32.AssignProcessToJobObject,@37")
#pragma comment(linker,"/export:AttachConsole=kernel32.AttachConsole,@38")
#pragma comment(linker,"/export:BackupRead=kernel32.BackupRead,@39")
#pragma comment(linker,"/export:BackupSeek=kernel32.BackupSeek,@40")
#pragma comment(linker,"/export:BackupWrite=kernel32.BackupWrite,@41")
#pragma comment(linker,"/export:BaseCheckAppcompatCache=kernel32.BaseCheckAppcompatCache,@42")
#pragma comment(linker,"/export:BaseCheckAppcompatCacheEx=kernel32.BaseCheckAppcompatCacheEx,@43")
#pragma comment(linker,"/export:BaseCheckAppcompatCacheExWorker=kernel32.BaseCheckAppcompatCacheExWorker,@44")
#pragma comment(linker,"/export:BaseCheckAppcompatCacheWorker=kernel32.BaseCheckAppcompatCacheWorker,@45")
#pragma comment(linker,"/export:BaseCheckElevation=kernel32.BaseCheckElevation,@46")
#pragma comment(linker,"/export:BaseCleanupAppcompatCacheSupport=kernel32.BaseCleanupAppcompatCacheSupport,@47")
#pragma comment(linker,"/export:BaseCleanupAppcompatCacheSupportWorker=kernel32.BaseCleanupAppcompatCacheSupportWorker,@48")
#pragma comment(linker,"/export:BaseDestroyVDMEnvironment=kernel32.BaseDestroyVDMEnvironment,@49")
#pragma comment(linker,"/export:BaseDllReadWriteIniFile=kernel32.BaseDllReadWriteIniFile,@50")
#pragma comment(linker,"/export:BaseDumpAppcompatCache=kernel32.BaseDumpAppcompatCache,@51")
#pragma comment(linker,"/export:BaseDumpAppcompatCacheWorker=kernel32.BaseDumpAppcompatCacheWorker,@52")
#pragma comment(linker,"/export:BaseElevationPostProcessing=kernel32.BaseElevationPostProcessing,@53")
#pragma comment(linker,"/export:BaseFlushAppcompatCache=kernel32.BaseFlushAppcompatCache,@54")
#pragma comment(linker,"/export:BaseFlushAppcompatCacheWorker=kernel32.BaseFlushAppcompatCacheWorker,@55")
#pragma comment(linker,"/export:BaseFormatObjectAttributes=kernel32.BaseFormatObjectAttributes,@56")
#pragma comment(linker,"/export:BaseFormatTimeOut=kernel32.BaseFormatTimeOut,@57")
#pragma comment(linker,"/export:BaseFreeAppCompatDataForProcessWorker=kernel32.BaseFreeAppCompatDataForProcessWorker,@58")
#pragma comment(linker,"/export:BaseGenerateAppCompatData=kernel32.BaseGenerateAppCompatData,@59")
#pragma comment(linker,"/export:BaseGetNamedObjectDirectory=kernel32.BaseGetNamedObjectDirectory,@60")
#pragma comment(linker,"/export:BaseInitAppcompatCacheSupport=kernel32.BaseInitAppcompatCacheSupport,@61")
#pragma comment(linker,"/export:BaseInitAppcompatCacheSupportWorker=kernel32.BaseInitAppcompatCacheSupportWorker,@62")
#pragma comment(linker,"/export:BaseIsAppcompatInfrastructureDisabled=kernel32.BaseIsAppcompatInfrastructureDisabled,@63")
#pragma comment(linker,"/export:BaseIsAppcompatInfrastructureDisabledWorker=kernel32.BaseIsAppcompatInfrastructureDisabledWorker,@64")
#pragma comment(linker,"/export:BaseIsDosApplication=kernel32.BaseIsDosApplication,@65")
#pragma comment(linker,"/export:BaseQueryModuleData=kernel32.BaseQueryModuleData,@66")
#pragma comment(linker,"/export:BaseReadAppCompatDataForProcessWorker=kernel32.BaseReadAppCompatDataForProcessWorker,@67")
#pragma comment(linker,"/export:BaseSetLastNTError=kernel32.BaseSetLastNTError,@68")
#pragma comment(linker,"/export:BaseThreadInitThunk=kernel32.BaseThreadInitThunk,@69")
#pragma comment(linker,"/export:BaseUpdateAppcompatCache=kernel32.BaseUpdateAppcompatCache,@70")
#pragma comment(linker,"/export:BaseUpdateAppcompatCacheWorker=kernel32.BaseUpdateAppcompatCacheWorker,@71")
#pragma comment(linker,"/export:BaseUpdateVDMEntry=kernel32.BaseUpdateVDMEntry,@72")
#pragma comment(linker,"/export:BaseVerifyUnicodeString=kernel32.BaseVerifyUnicodeString,@73")
#pragma comment(linker,"/export:BaseWriteErrorElevationRequiredEvent=kernel32.BaseWriteErrorElevationRequiredEvent,@74")
#pragma comment(linker,"/export:Basep8BitStringToDynamicUnicodeString=kernel32.Basep8BitStringToDynamicUnicodeString,@75")
#pragma comment(linker,"/export:BasepAllocateActivationContextActivationBlock=kernel32.BasepAllocateActivationContextActivationBlock,@76")
#pragma comment(linker,"/export:BasepAnsiStringToDynamicUnicodeString=kernel32.BasepAnsiStringToDynamicUnicodeString,@77")
#pragma comment(linker,"/export:BasepAppContainerEnvironmentExtension=kernel32.BasepAppContainerEnvironmentExtension,@78")
#pragma comment(linker,"/export:BasepAppXExtension=kernel32.BasepAppXExtension,@79")
#pragma comment(linker,"/export:BasepCheckAppCompat=kernel32.BasepCheckAppCompat,@80")
#pragma comment(linker,"/export:BasepCheckWebBladeHashes=kernel32.BasepCheckWebBladeHashes,@81")
#pragma comment(linker,"/export:BasepCheckWinSaferRestrictions=kernel32.BasepCheckWinSaferRestrictions,@82")
#pragma comment(linker,"/export:BasepConstructSxsCreateProcessMessage=kernel32.BasepConstructSxsCreateProcessMessage,@83")
#pragma comment(linker,"/export:BasepCopyEncryption=kernel32.BasepCopyEncryption,@84")
#pragma comment(linker,"/export:BasepFreeActivationContextActivationBlock=kernel32.BasepFreeActivationContextActivationBlock,@85")
#pragma comment(linker,"/export:BasepFreeAppCompatData=kernel32.BasepFreeAppCompatData,@86")
#pragma comment(linker,"/export:BasepGetAppCompatData=kernel32.BasepGetAppCompatData,@87")
#pragma comment(linker,"/export:BasepGetComputerNameFromNtPath=kernel32.BasepGetComputerNameFromNtPath,@88")
#pragma comment(linker,"/export:BasepGetExeArchType=kernel32.BasepGetExeArchType,@89")
#pragma comment(linker,"/export:BasepInitAppCompatData=kernel32.BasepInitAppCompatData,@90")
#pragma comment(linker,"/export:BasepIsProcessAllowed=kernel32.BasepIsProcessAllowed,@91")
#pragma comment(linker,"/export:BasepMapModuleHandle=kernel32.BasepMapModuleHandle,@92")
#pragma comment(linker,"/export:BasepNotifyLoadStringResource=kernel32.BasepNotifyLoadStringResource,@93")
#pragma comment(linker,"/export:BasepPostSuccessAppXExtension=kernel32.BasepPostSuccessAppXExtension,@94")
#pragma comment(linker,"/export:BasepProcessInvalidImage=kernel32.BasepProcessInvalidImage,@95")
#pragma comment(linker,"/export:BasepQueryAppCompat=kernel32.BasepQueryAppCompat,@96")
#pragma comment(linker,"/export:BasepQueryModuleChpeSettings=kernel32.BasepQueryModuleChpeSettings,@97")
#pragma comment(linker,"/export:BasepReleaseAppXContext=kernel32.BasepReleaseAppXContext,@98")
#pragma comment(linker,"/export:BasepReleaseSxsCreateProcessUtilityStruct=kernel32.BasepReleaseSxsCreateProcessUtilityStruct,@99")
#pragma comment(linker,"/export:BasepReportFault=kernel32.BasepReportFault,@100")
#pragma comment(linker,"/export:BasepSetFileEncryptionCompression=kernel32.BasepSetFileEncryptionCompression,@101")
#pragma comment(linker,"/export:Beep=kernel32.Beep,@102")
#pragma comment(linker,"/export:BeginUpdateResourceA=kernel32.BeginUpdateResourceA,@103")
#pragma comment(linker,"/export:BeginUpdateResourceW=kernel32.BeginUpdateResourceW,@104")
#pragma comment(linker,"/export:BindIoCompletionCallback=kernel32.BindIoCompletionCallback,@105")
#pragma comment(linker,"/export:BuildCommDCBA=kernel32.BuildCommDCBA,@106")
#pragma comment(linker,"/export:BuildCommDCBAndTimeoutsA=kernel32.BuildCommDCBAndTimeoutsA,@107")
#pragma comment(linker,"/export:BuildCommDCBAndTimeoutsW=kernel32.BuildCommDCBAndTimeoutsW,@108")
#pragma comment(linker,"/export:BuildCommDCBW=kernel32.BuildCommDCBW,@109")
#pragma comment(linker,"/export:CallNamedPipeA=kernel32.CallNamedPipeA,@110")
#pragma comment(linker,"/export:CallNamedPipeW=kernel32.CallNamedPipeW,@111")
#pragma comment(linker,"/export:CallbackMayRunLong=kernel32.CallbackMayRunLong,@112")
#pragma comment(linker,"/export:CancelDeviceWakeupRequest=kernel32.CancelDeviceWakeupRequest,@113")
#pragma comment(linker,"/export:CancelIo=kernel32.CancelIo,@114")
#pragma comment(linker,"/export:CancelIoEx=kernel32.CancelIoEx,@115")
#pragma comment(linker,"/export:CancelSynchronousIo=kernel32.CancelSynchronousIo,@116")
#pragma comment(linker,"/export:CancelThreadpoolIo=kernel32.CancelThreadpoolIo,@117")
#pragma comment(linker,"/export:CancelTimerQueueTimer=kernel32.CancelTimerQueueTimer,@118")
#pragma comment(linker,"/export:CancelWaitableTimer=kernel32.CancelWaitableTimer,@119")
#pragma comment(linker,"/export:CeipIsOptedIn=kernel32.CeipIsOptedIn,@120")
#pragma comment(linker,"/export:ChangeTimerQueueTimer=kernel32.ChangeTimerQueueTimer,@121")
#pragma comment(linker,"/export:CheckAllowDecryptedRemoteDestinationPolicy=kernel32.CheckAllowDecryptedRemoteDestinationPolicy,@122")
#pragma comment(linker,"/export:CheckElevation=kernel32.CheckElevation,@123")
#pragma comment(linker,"/export:CheckElevationEnabled=kernel32.CheckElevationEnabled,@124")
#pragma comment(linker,"/export:CheckForReadOnlyResource=kernel32.CheckForReadOnlyResource,@125")
#pragma comment(linker,"/export:CheckForReadOnlyResourceFilter=kernel32.CheckForReadOnlyResourceFilter,@126")
#pragma comment(linker,"/export:CheckNameLegalDOS8Dot3A=kernel32.CheckNameLegalDOS8Dot3A,@127")
#pragma comment(linker,"/export:CheckNameLegalDOS8Dot3W=kernel32.CheckNameLegalDOS8Dot3W,@128")
#pragma comment(linker,"/export:CheckRemoteDebuggerPresent=kernel32.CheckRemoteDebuggerPresent,@129")
#pragma comment(linker,"/export:CheckTokenCapability=kernel32.CheckTokenCapability,@130")
#pragma comment(linker,"/export:CheckTokenMembershipEx=kernel32.CheckTokenMembershipEx,@131")
#pragma comment(linker,"/export:ClearCommBreak=kernel32.ClearCommBreak,@132")
#pragma comment(linker,"/export:ClearCommError=kernel32.ClearCommError,@133")
#pragma comment(linker,"/export:CloseConsoleHandle=kernel32.CloseConsoleHandle,@134")
#pragma comment(linker,"/export:CloseHandle=kernel32.CloseHandle,@135")
...................................
```

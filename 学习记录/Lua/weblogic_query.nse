--author:jiushi
--date:19-7-10
--time:早上9:28

local http=require "http"
local shortport=require "shortport"
local stdnse=require "stdnse"
local string=require "string"
local vulns=require "vulns"

description=[[
Weblogic path scanning
]]

--nmap --script=weblogic_query --script-args port=<weblogic_port>,protocol=<http/https> IP
--Starting Nmap 7.70 ( https://nmap.org ) at 2019-07-10 12:59 CST
--Nmap scan report for 192.168.241.140
--Host is up (0.00021s latency).

--PORT     STATE SERVICE
--7001/tcp open  afs3-callback
--| weblogic_query:
--|   [200]: http://192.168.241.140:7001/console/login/LoginForm.jsp
--|   [200]: http://192.168.241.140:7001/wls-wsat/CoordinatorPortType
--|   [200]: http://192.168.241.140:7001/_async/AsyncResponseService
--|_  [200]: http://192.168.241.140:7001/uddiexplorer

--Nmap done: 1 IP address (1 host up) scanned in 2.45 seconds


author="Jiushi"
license="Same as Nmap--See https://nmap.org/book/man-legal.html"
categories={"default"}

portrule=function(host,port)
	set_port=stdnse.get_script_args("port")
	if (type(set_port)~="nil") then
		local auth_port={number=tonumber(set_port),protocol="tcp"}
		local identd=nmap.get_port_state(host,auth_port)
		return identd.number==tonumber(set_port) and identd.state=="open" and port.protocol=="tcp"

	end
end

function jianche(url,path)
	local demo={}
	local headers={header={}}
	headers['header']['User-Agent']="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
	for p in pairs(path) do
		local urls=string.format("%s:%s%s",url,set_port,path[p])
		local request=http.get_url(urls,headers)
		if (request.status==200 and string.match(request.body,"Not Found")==nil) then
			table.insert(demo,string.format("[%s]: %s",request.status,urls))
		end

	end
	return demo
end

action=function(host,port)
	local ht=stdnse.get_script_args("protocol")
	local path={"/console/login/LoginForm.jsp","/wls-wsat/CoordinatorPortType","/_async/AsyncResponseService","/ws_utc/config.do","/uddiexplorer"}
	local urls=string.format("%s://%s",ht,host['ip'])
	local jiances=jianche(urls,path)
	return jiances

end

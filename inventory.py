import re
import glob

def parse_version(path):
    with open(path) as f:
        text=f.read()
    a= re.search(r"Cisco IOS XE Software, Version (?P<version>\S+)",text)
    b = re.search(r"(?P<hostname>\S+) uptime is .+",text)
    # lowercase "cisco" + space: skips "www.cisco.com" (no space) and "Cisco Systems" (capital C)
    c= re.search(r"cisco (?P<model>\S+)\s+\S+\s+processor\s.+",text)
    d= re.search(r"Processor board ID (?P<serial>\S+)",text)

    device={}
    for m in (b,a,c,d):
        if m:
            device.update(m.groupdict())
    return device



files= glob.glob("devices/*.txt")
files=sorted(files)
with open("inventory.csv","w") as f:
    f.write("hostname,version,model,serial\n") 
    for file in files:
            result = parse_version(file)
            f.write(f"{result['hostname']},{result['version']},{result['model']},{result['serial']}\n")
            if int(result['version'].split(".")[0]) < 17:
                 print(f"WARNING: {result['hostname']} runs {result['version']} (below 17)")

print(f"{len(files)} devices written to inventory.csv")
# print(parse_version("devices/R1-MUM-EDGE_show_version.txt"))
# print(parse_version("devices/R2-PUN-CORE_show_version.txt"))
# print(parse_version("devices/SW1-MUM-ACC_show_version.txt"))


# Cisco IOS XE Software, Version 17.09.04a
# Cisco IOS Software [Cupertino], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 17.9.4a, RELEASE SOFTWARE (fc3)
# Technical Support: http://www.cisco.com/techsupport
# Copyright (c) 1986-2023 by Cisco Systems, Inc.

# ROM: IOS-XE ROMMON

# R1-MUM-EDGE uptime is 12 weeks, 3 days, 4 hours, 18 minutes
# Uptime for this control processor is 12 weeks, 3 days, 4 hours, 20 minutes
# System returned to ROM by reload
# System image file is "bootflash:packages.conf"

# cisco C8000V (VXE) processor (revision VXE) with 1987654K/3075K bytes of memory.
# Processor board ID 9ABCDEF1234
# 4 Gigabit Ethernet interfaces
# 32768K bytes of non-volatile configuration memory.

# Configuration register is 0x2102
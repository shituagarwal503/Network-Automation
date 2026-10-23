import re


def check_interfaces(file_name):
    interfaces = {}
    current = {}
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            if 'line protocol' in line:
                m = re.search(r"(\S+) is (.+), line protocol is (\S+)", line)
                if m:
                    current.update({"interface": m.group(1), "admin_status": m.group(2), "line_status": m.group(3)})

            if 'MTU' in line:
                m = re.search(r"MTU (\d+) bytes", line)
                if m:
                    current["mtu"] = int(m.group(1))

            if 'CRC' in line:
                m = re.search(r"(\d+) input errors, (\d+) CRC", line)
                if m:
                    current["input_errors"] = int(m.group(1))
                    current["crc"] = int(m.group(2))
                    # the CRC line is the last one we need, so this interface is complete
                    interfaces[current["interface"]] = current
                    current = {}
    return interfaces


interfaces = check_interfaces("interfaces.txt")
issues = 0

# one loop per issue type, so the output is grouped: DOWN, ADMIN-DOWN, CRC, JUMBO
for name in interfaces:
    intf = interfaces[name]
    if intf["line_status"] == "down" and intf["admin_status"] != "administratively down":
        print(f"DOWN: {name} status={intf['admin_status']} protocol={intf['line_status']}")
        issues += 1
for name in interfaces:
    if interfaces[name]["admin_status"] == "administratively down":
        print(f"ADMIN-DOWN: {name}")
        issues += 1
for name in interfaces:
    intf = interfaces[name]
    if intf["crc"] > 0:
        print(f"CRC: {name} crc={intf['crc']} input_errors={intf['input_errors']}")
        issues += 1
for name in interfaces:
    # loopbacks are virtual, 1514 is their default MTU, so skip them
    if interfaces[name]["mtu"] != 1500 and not name.startswith("Loopback"):
        print(f"JUMBO: {name} mtu={interfaces[name]['mtu']}")
        issues += 1
print(f"{issues} issues on {len(interfaces)} interfaces")

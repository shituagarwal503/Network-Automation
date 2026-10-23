import re
import glob


def parse_version(path):
    with open(path) as f:
        text = f.read()
    version_m = re.search(r"Cisco IOS XE Software, Version (?P<version>\S+)", text)
    hostname_m = re.search(r"(?P<hostname>\S+) uptime is", text)
    # lowercase "cisco" + space: skips "www.cisco.com" (no space) and "Cisco Systems" (capital C)
    model_m = re.search(r"cisco (?P<model>\S+)", text)
    serial_m = re.search(r"Processor board ID (?P<serial>\S+)", text)

    device = {}
    for m in (hostname_m, version_m, model_m, serial_m):
        if m:
            device.update(m.groupdict())
    return device


files = sorted(glob.glob("devices/*.txt"))
with open("inventory.csv", "w") as f:
    f.write("hostname,version,model,serial\n")
    for path in files:
        device = parse_version(path)
        f.write(f"{device['hostname']},{device['version']},{device['model']},{device['serial']}\n")
        if int(device["version"].split(".")[0]) < 17:
            print(f"WARNING: {device['hostname']} runs {device['version']} (below 17)")

print(f"{len(files)} devices written to inventory.csv")

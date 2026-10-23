import re


def parse_ip_brief(file_name):
    with open(file_name) as f:
        # one tuple per interface: (name, ip, status, protocol); the header doesn't match
        return re.findall(r"(\S+)\s+(\S+)\s+\S+\s+\S+\s+(up|down|administratively down)\s+(up|down)", f.read())


interfaces = parse_ip_brief("ip_brief.txt")
admin_down_count, down_count = 0, 0
with open("report.txt", "w") as f:
    for intf in interfaces:
        if "administratively down" in intf:
            admin_down_count += 1
        elif "down" in intf:
            f.write(f"DOWN: {intf[0]} ip={intf[1]} status={intf[2]} protocol={intf[3]}\n")
            down_count += 1
    f.write(f"{down_count} down, {admin_down_count} admin-down, {len(interfaces)} total\n")

with open("report.txt") as f:
    print(f.read().strip())

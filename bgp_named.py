import re


def check_bgp(file_name):
    header_found = False
    neighbors = []
    with open(file_name) as f:
        for line in f:
            if header_found:
                line = line.strip()
                m = re.search(r"^(?P<ip>\S+)\s+\d+\s+(?P<remote_as>\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(?P<uptime>\S+)\s+(?P<state>.+)$", line)
                if m:
                    neighbors.append(m.groupdict())
            if line.startswith("Neighbor"):
                header_found = True
    return neighbors


neighbors = check_bgp("bgp.txt")
for n in neighbors:
    if n["state"].isdigit() and int(n["state"]) != 0:
        print(f"{n['ip']} AS{n['remote_as']} Established ({n['state']} prefixes)")
    elif n["state"].isdigit() and int(n["state"]) == 0:
        print(f"{n['ip']} AS{n['remote_as']} Established ({n['state']} prefixes) WARNING")
    else:
        print(f"{n['ip']} AS{n['remote_as']} {n['state']}")

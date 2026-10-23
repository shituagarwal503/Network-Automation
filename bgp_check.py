import re


def check_bgp(file_name):
    header_found = False
    down = 0
    total = 0
    down_neighbors = []
    warnings = []
    with open(file_name) as f:
        for line in f:
            if header_found:
                line = line.strip()
                m = re.search(r"^(\S+)\s+\d+\s+(\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\S+\s+(.+)$", line)
                if m:
                    total += 1
                    ip = m.group(1)
                    remote_as = m.group(2)
                    state = m.group(3)
                    if not state.isdigit():
                        down += 1
                        down_neighbors.append([ip, remote_as, state])
                    elif int(state) == 0:
                        # a number in State/PfxRcd means Established, so it isn't down;
                        # but 0 prefixes received is worth investigating
                        # (an inbound prefix-list, or the neighbour not advertising)
                        warnings.append(f"WARNING: {ip} (AS {remote_as}) Established but {state} prefixes received")

            if line.startswith("Neighbor"):
                header_found = True

    return down, total, down_neighbors, warnings


down, total, down_neighbors, warnings = check_bgp("bgp.txt")
for neighbor in down_neighbors:
    print(f"DOWN: {neighbor[0]} (AS {neighbor[1]}) state={neighbor[2]}")
for warning in warnings:
    print(warning)
print(f"{down} of {total} neighbours not Established")

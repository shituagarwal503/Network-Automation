import re


def check_bgp(file_name):
    header_found = False
    down=0
    total=0
    with open(file_name) as f:
        w,j=[],[]
        for line in f:
            if header_found:
                line=line.strip()
                m=re.search(r"^(\S+)\s+\d+\s+(\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\S+\s+(.+)$",line)
                if m:
                    total+=1
                    ip = m.group(1)
                    remote_as = m.group(2)
                    state = m.group(3)
                    if not state.isdigit():
                        down+=1
                        l=[]
                        l.append(ip)
                        l.append(remote_as)
                        l.append(state)
                        w.append(l)
                    elif int(state) == 0:
                        # the number in State/PfxRcd means Established,
                        # so the script correctly doesn't report it as down;
                        # but 0 prefixes after 2 weeks up is worth investigating
                        # (an inbound prefix-list, or the neighbour not advertising). 
                        j.append(f"WARNING: {ip} (AS {remote_as}) Established but {state} prefixes received")    
                                       
            if line.startswith('Neighbor'):
                header_found=True

    return down,total,w,j

    
down,total,w,j=  check_bgp("bgp.txt")
for i in range(0,len(w)):
    print(f"DOWN: {w[i][0]} (AS {w[i][1]}) state={w[i][2]}")
for i in j:
    print(i)
print(f"{down} of {total} neighbours not Established")
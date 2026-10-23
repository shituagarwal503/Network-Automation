import re

def check_bgp(file_name):
    l=[]
    with open(file_name) as f:
        for line in f:
            line=line.strip()
            m=re.search(r"^(?P<ip>\S+)\s+\d+\s+(?P<remote_as>\d+)\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(?P<status>\S+)\s+(?P<state>.+)$",line)
            if m:
                l.append(m.groupdict())
    return l

result = check_bgp("bgp.txt")
for i in result:
     if i['state'].isdigit() and int(i['state'])!=0:
        print(f"{i['ip']} AS{i['remote_as']} Established ({i['state']} prefixes)")
     elif i['state'].isdigit() and int(i['state'])==0:
         print(f"{i['ip']} AS{i['remote_as']} Established ({i['state']} prefixes) WARNING")
     else:
        print(f"{i['ip']} AS{i['remote_as']} {i['state']}")



import re
import copy

def check_interfaces(file_name):
    with open(file_name) as f:
            k,y={},{}
            for i in f:
                i= i.strip()
                if 'line protocol' in i:
                    q=re.search(r"(\S+) is (.+), line protocol is (\S+)", i)
                    interface= q.group(1)
                    admin_status =  q.group(2)
                    line_status = q.group(3)
                    y.update({"interface":interface,"admin_status":admin_status,"line_status":line_status})
                    # y.append(interface)
                    # y.append(admin_status)
                    # y.append(line_status)

                if 'MTU' in i:
                    q=re.search(r"MTU (\d+) bytes, BW (\d+) Kbit/sec, DLY (\d+) usec,",i)
                    mtu_value=q.group(1)
                    y.update({"mtu_value":mtu_value})
                    # y.append(int(mtu_value))

                if 'CRC' in i:
                    q=re.search(r"(\d+) input errors, (\d+) CRC, (\d+) frame, (\d+) overrun, (\d+) ignored",i)
                    Error= q.group(1)
                    mv=q.group(2)
                    y.update({'Error':Error,"mv":mv})
                    # y.append(Error)
                    # y.append(mv)
                    k[interface]=y
                    y={}
    return k            
                


result = check_interfaces("interfaces.txt")
n=0

# one loop per issue type, so the output is grouped: DOWN, ADMIN-DOWN, CRC, JUMBO
for item in result:
    if result[item]['admin_status']=='down' or result[item]['line_status']!='administratively down':
        print(f"DOWN: {result[item]['interface']} status={result[item]['admin_status']} protocol={result[item]['line_status']}")
        n+=1
    if int(result[item]['mv'])>0:
        print(f"CRC: {result[item]['interface']} crc={result[item]['mv']} input_errors={result[item]['Error']}")
        n+=1
    # loopbacks are virtual, 1514 is their default MTU, so skip them
    if result[item]['mtu_value']!= '1500' and not result[item]['interface'].startswith("Loopback"):
        print(f"JUMBO: {result[item]['interface']} mtu={result[item]['mtu_value']}")
        n+=1
print(f"{n} issues on {len(result)} interfaces")




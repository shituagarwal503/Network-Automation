import re

def find_down(file_name):

    with open(file_name) as f:
        q= re.findall(r"(\S+)\s+(\S+)\s+\S+\s+\S+\s+(up|down|administratively down)\s+(up|down)",f.read())
        return q




result=find_down("ip_brief.txt")
w,e=0,0
with open("report.txt","w") as f:
    for i in result:
        if 'administratively down' in i:
            w=w+1
        elif 'down' in i:
            # print(f"DOWN: {i[0]} ip={i[1]} status={i[2]} protocol={i[3]}")

            f.write(f"DOWN: {i[0]} ip={i[1]} status={i[2]} protocol={i[3]}\n")
            e=e+1
    f.write(f"{e} down, {w} admin-down, {len(result)} total\n")

with open("report.txt") as f:
    print(f.read())
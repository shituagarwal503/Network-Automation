import re

def sanitize(in_file,out_file):
    with open(in_file) as f:
        n=0
        with open(out_file,"w") as q:
            for l in f:
                print(f"l======>{l}")
                s = re.sub(r"(secret|password|key)\s+(\d+)(.+)$",r"\1 \2 <removed>",l)
                print(f"s------>{s}")
                t= re.sub(r"(community)\s(\S+)\s(\S+)",r"\1 <removed> \3",s)   
                print(f"t----->{t}")            
                if t!=l:
                    n+=1
                q.write(t)
        return n





n=sanitize(in_file='running_config.txt',out_file="running_config_clean.txt")
print(f"masked {n}")
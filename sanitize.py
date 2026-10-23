import re


def sanitize(in_file, out_file):
    masked = 0
    with open(in_file) as in_f, open(out_file, "w") as out_f:
        for line in in_f:
            # keep the keyword and type digit, e.g. "secret 5 <removed>"
            clean = re.sub(r"(secret|password|key)\s+(\d+)(.+)$", r"\1 \2 <removed>", line)
            # SNMP communities have no type digit: "community <removed> RO"
            clean = re.sub(r"(community)\s(\S+)\s(\S+)", r"\1 <removed> \3", clean)
            if clean != line:
                masked += 1
            # write every line, changed or not, so the config stays complete
            out_f.write(clean)
    return masked


masked = sanitize(in_file="running_config.txt", out_file="running_config_clean.txt")
print(f"masked {masked}")

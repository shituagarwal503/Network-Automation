# Network Automation Practice

Python scripts that parse Cisco IOS / IOS XE command output and flag problems, the kind of checks a network test engineer does by hand during validation. All data files are lab samples; no production configs.

## Scripts

| Script | Input | What it does |
|---|---|---|
| `bgp_check.py` | `bgp.txt` (`show ip bgp summary`) | Lists BGP neighbours that aren't Established, and warns on sessions that are Established but receiving 0 prefixes |
| `bgp_named.py` | `bgp.txt` | Same parsing using regex named groups and dicts; prints every neighbour's state and prefix count |
| `interface_check.py` | `interfaces.txt` (`show interfaces`) | Parses multi-line interface blocks; reports DOWN, ADMIN-DOWN, CRC errors and non-standard MTU (skipping loopbacks) |
| `ip_brief_check.py` | `ip_brief.txt` (`show ip interface brief`) | Parses the whole table with one `re.findall`, separates down from admin-down, writes `report.txt` |
| `sanitize.py` | `running_config.txt` | Masks passwords, secrets, keys and SNMP communities with `re.sub` before a config is shared; writes `running_config_clean.txt` |
| `inventory.py` | `devices/*.txt` (`show version`) | Parses hostname, version, model and serial from every device file found with `glob`; writes `inventory.csv` and flags IOS XE versions below 17 |

## Run

Python 3.10 or later, standard library only:

```
python bgp_check.py
python inventory.py
```

## Skills practised

File handling, regular expressions (`search`, `findall`, `sub`, named groups), functions that return data, lists and dicts, CSV output, `glob`.

## Next

Netmiko: running the same checks against live lab devices instead of saved output.

import sys
import re
import json


class Config:
    """captures run configuration"""

    def __init__(self, cfgdict):
        self.logfile = cfgdict["logfile"]
        self.top_req_pages = cfgdict["top_req_pages"]
        self.perc_succ_reqs = cfgdict["perc_succ_reqs"]
        self.perc_fail_reqs = cfgdict["perc_fail_reqs"]
        self.top_hosts = cfgdict["top_hosts"]
        self.top_pages_per_host = cfgdict["top_pages_per_host"]
        self.error_in_lines = cfgdict["error_in_lines"]


def stats(config):
    """
    Read log file and keep stats as you go along.
    This is linear and not multicore.
    We can follow a map-reduce approach if we break up the log file
    (more on the second part of the take home assignment).
    """
    res = {
        "top_req_pages": [],
        "perc_succ_reqs": 0,
        "perc_fail_reqs": 0,
        "top_hosts": [],
        "error_in_lines": None,
    }
    # reg exp that parses general log format. Some groups are optional (?)
    p = re.compile(r'(.*)\s-\s-\s\[(.*)\]\s"(\w+)\s(.*)(\s.*)?"\s(\d+)\s(\d+)?')
    lineno = 0
    # that's the basic stats index based on hosts
    hosts = {}
    # secondary index to help with pages stats
    pages = {}
    # another index to keep error lines
    errors = []
    lineno = 0
    with open(config.logfile, "r", errors="replace") as logf:
        # Can't do better than O(n) - we need to read through all log file
        for line in logf:
            lineno += 1
            try:
                m = p.match(line)
                # unpack parsed values - nbytes is optional
                nbytes = 0
                if len(m.groups()) == 7:
                    host, t, verb, page, vers, status, nbytes = m.groups()
                elif len(m.groups()) == 6:
                    host, t, verb, page, vers, status = m.groups()
                else:
                    errors.append(lineno)
                    continue
                # keep pages-based stats
                if page not in pages:
                    pages[page] = {"count": 1, "fails": 0}
                else:
                    pages[page]["count"] += 1
                # keep hosts-based stats...
                if host not in hosts:
                    hosts[host] = {"count": 1, "fails": 0, "pages": {page: 1}}
                else:
                    hosts[host]["count"] += 1
                    # ...keep stats that relate hosts to pages
                    if page not in hosts[host]["pages"]:
                        hosts[host]["pages"][page] = 1
                    else:
                        hosts[host]["pages"][page] += 1
                # ...and stats relating hosts to http errors
                if int(status) >= 400 or int(status) < 200:
                    hosts[host]["fails"] += 1
                    pages[page]["fails"] += 1
            # any error contributes to errors index
            except (UnicodeDecodeError, AttributeError):
                errors.append(lineno)
                continue
    # extract stats for pages
    pages_freq = sorted(pages.keys(), key=lambda x: pages[x]["count"], reverse=True)
    for p in pages_freq[: config.top_req_pages]:
        res["top_req_pages"].append((p, pages[p]["count"]))
    # extract success/failure rates
    fails, total = 0, 0
    for h in hosts:
        fails += hosts[h]["fails"]
        total += hosts[h]["count"]
    succ = total - fails
    res["perc_succ_reqs"] = f"{100 * succ/total:.2f}"
    res["perc_fail_reqs"] = f"{100 * fails/total:.2f}"
    # extract host-based stats
    hosts_freq = sorted(hosts.keys(), key=lambda x: hosts[x]["count"], reverse=True)
    # get config.top_hosts most active hosts
    for h in hosts_freq[: config.top_hosts]:
        res["top_hosts"].append(
            {"host": h, "count": hosts[h]["count"], "breakdown": []}
        )
        pages_freq_for_host = sorted(
            hosts[h]["pages"].keys(), key=lambda x: hosts[h]["pages"][x], reverse=True
        )
        # get top config.top_pages_per_host pages breakdown for host
        for p in pages_freq_for_host[: config.top_pages_per_host]:
            res["top_hosts"][-1]["breakdown"].append((p, hosts[h]["pages"][p]))
    # errors
    res["error_in_lines"] = errors
    # all stats return as a dictionary
    return res


def main():
    # read in config for this run
    with open("config.json") as json_file:
        config = Config(cfgdict=json.load(json_file))
        res = stats(config=config)
        print(json.dumps(res, indent=4))


if __name__ == "__main__":
    main()

from distutils.log import Log
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


class LogLine:
    """Captures an analysed log line"""

    # static - compiled once
    MATCHER = re.compile(r'(.*)\s-\s-\s\[(.*)\]\s"(.*)"\s(.*)')

    # ctor
    def __init__(self, line):
        try:
            # match line against reg exp
            m = self.MATCHER.match(line)
            self.host = m.group(1)
            self.time = m.group(2)
            self.version = None
            verb_page_version = m.group(3).split()
            if len(verb_page_version) == 3:
                self.verb, self.page, self.version = verb_page_version
            else:
                self.verb, self.page = verb_page_version
            status_nbytes = m.group(4).split()
            if len(status_nbytes) == 2:
                self.status, self.nbytes = status_nbytes
            else:
                self.status = status_nbytes[0]
                self.nbytes = "0"
            self.status = int(self.status)
            # treat garbage in nbytes
            for c in self.nbytes:
                if not c.isdigit():
                    self.nbytes = 0
                    return
            self.nbytes = int(self.nbytes)
        except Exception:
            raise


class Stats:
    """Calculates statistics for a log file according to run configuration"""

    def __init__(self, config):
        # run configuration for this instance
        self.config = config
        # that's the basic stats index based on hosts
        self.hosts = {}
        # secondary index to help with pages stats
        self.pages = {}
        # another index to keep error lines
        self.errors = []

    def _calc_indexes(self):
        """
        Read log file and keep stats as you go along.
        This is linear and not multicore.
        We can follow a map-reduce approach if we break up the log file
        (more on the second part of the take home assignment).
        """
        lineno = 0
        with open(self.config.logfile, "r", errors="replace") as logf:
            # Can't do better than O(n) - we need to read through all log file
            for line in logf:
                lineno += 1
                try:
                    lg = LogLine(line=line)
                    # keep pages-based stats
                    if lg.page not in self.pages:
                        self.pages[lg.page] = {"count": 1, "fails": 0}
                    else:
                        self.pages[lg.page]["count"] += 1
                    # keep hosts-based stats...
                    if lg.host not in self.hosts:
                        self.hosts[lg.host] = {
                            "count": 1,
                            "fails": 0,
                            "pages": {lg.page: 1},
                        }
                    else:
                        self.hosts[lg.host]["count"] += 1
                        # ...keep stats that relate hosts to pages
                        if lg.page not in self.hosts[lg.host]["pages"]:
                            self.hosts[lg.host]["pages"][lg.page] = 1
                        else:
                            self.hosts[lg.host]["pages"][lg.page] += 1
                    # ...and stats relating hosts to http errors
                    if int(lg.status) >= 400 or int(lg.status) < 200:
                        self.hosts[lg.host]["fails"] += 1
                        self.pages[lg.page]["fails"] += 1
                # any error contributes to errors index
                except (UnicodeDecodeError, AttributeError):
                    self.errors.append(lineno)
                    continue

    def _calc_stats(self):
        """Calculate statistics based on the pages and host indexes"""
        res = {
            "top_req_pages": [],
            "perc_succ_reqs": 0,
            "perc_fail_reqs": 0,
            "top_hosts": [],
            "error_in_lines": None,
        }

        # extract stats for pages
        pages_freq = sorted(
            self.pages.keys(), key=lambda x: self.pages[x]["count"], reverse=True
        )
        for p in pages_freq[: self.config.top_req_pages]:
            res["top_req_pages"].append((p, self.pages[p]["count"]))
        # extract success/failure rates
        fails, total = 0, 0
        for h in self.hosts:
            fails += self.hosts[h]["fails"]
            total += self.hosts[h]["count"]
        succ = total - fails
        res["perc_succ_reqs"] = f"{100 * succ/total:.2f}"
        res["perc_fail_reqs"] = f"{100 * fails/total:.2f}"
        # extract host-based stats
        hosts_freq = sorted(
            self.hosts.keys(), key=lambda x: self.hosts[x]["count"], reverse=True
        )
        # get config.top_hosts most active hosts
        for h in hosts_freq[: self.config.top_hosts]:
            res["top_hosts"].append(
                {"host": h, "count": self.hosts[h]["count"], "breakdown": []}
            )
            pages_freq_for_host = sorted(
                self.hosts[h]["pages"].keys(),
                key=lambda x: self.hosts[h]["pages"][x],
                reverse=True,
            )
            # get top config.top_pages_per_host pages breakdown for host
            for p in pages_freq_for_host[: self.config.top_pages_per_host]:
                res["top_hosts"][-1]["breakdown"].append((p, self.hosts[h]["pages"][p]))
        # errors
        res["error_in_lines"] = self.errors
        # all stats return as a dictionary
        return res

    def stats(self):
        self._calc_indexes()
        return self._calc_stats()


def main():
    # read in config for this run
    with open("config.json") as json_file:
        config = Config(cfgdict=json.load(json_file))
        stats = Stats(config=config)
        res = stats.stats()
        print(json.dumps(res, indent=4))


if __name__ == "__main__":
    main()

import unittest
import json
from src.ireadlogs.stats import Stats
from src.ireadlogs.runconfig import RunConfig


class TestLogStats(unittest.TestCase):
    def test_calc_indexes(self):
        cfg = RunConfig(
        {
            "logfile": "tests/resources/logfile.txt",
            "top_req_pages": 5,
            "perc_succ_reqs": True,
            "perc_fail_reqs": True,
            "top_hosts": 5,
            "top_pages_per_host": 5,
            "show_errors": True,
        }
        )
        st = Stats(config=cfg)
        st._calc_indexes()
        with open("tests/resources/logfile_hosts.json") as inf:
            want_hosts = json.load(inf)
        with open("tests/resources/logfile_pages.json") as inf:
            want_pages = json.load(inf)
        self.assertEqual(st.hosts, want_hosts)
        self.assertEqual(st.pages, want_pages)
        self.assertEqual(st.errors, [6])

    def test_calc_stats(self):
        cfg = RunConfig(
        {
            "logfile": "tests/resources/logfile2.txt",
            "top_req_pages": 5,
            "perc_succ_reqs": True,
            "perc_fail_reqs": True,
            "top_hosts": 5,
            "top_pages_per_host": 5,
            "show_errors": True,
        }
        )
        st = Stats(config=cfg)
        st._calc_indexes()
        stats = st._calc_stats()
        self.assertEqual(stats['top_req_pages'][0][0], "/home")
        self.assertEqual(stats['top_hosts'][0]['host'], "uplherc.upl.com")
        self.assertEqual(stats['top_hosts'][0]['count'], 5)

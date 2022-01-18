import unittest
from src.ireadlogs.runconfig import RunConfig


class TestLogStats(unittest.TestCase):
    def test_config(self):
        cfg = {
            "logfile": "NASA_access_log_Aug95",
            "top_req_pages": 2,
            "perc_succ_reqs": True,
            "perc_fail_reqs": True,
            "top_hosts": 2,
            "top_pages_per_host": 5,
            "show_errors": True,
        }
        UAT = RunConfig(cfgdict=cfg)
        self.assertEqual(UAT.logfile, cfg["logfile"])
        self.assertEqual(UAT.top_req_pages, cfg["top_req_pages"])
        self.assertEqual(UAT.perc_succ_reqs, cfg["perc_succ_reqs"])
        self.assertEqual(UAT.perc_fail_reqs, cfg["perc_fail_reqs"])
        self.assertEqual(UAT.top_hosts, cfg["top_hosts"])
        self.assertEqual(UAT.top_pages_per_host, cfg["top_pages_per_host"])
        self.assertEqual(UAT.show_errors, cfg["show_errors"])

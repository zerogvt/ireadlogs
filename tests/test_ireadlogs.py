import unittest
from ireadlogs.ireadlogs import Config, LogLine


class TestLogStats(unittest.TestCase):
    def test_config(self):
        cfg = {
            "logfile": "NASA_access_log_Aug95",
            "top_req_pages": 2,
            "perc_succ_reqs": True,
            "perc_fail_reqs": True,
            "top_hosts": 2,
            "top_pages_per_host": 5,
            "error_in_lines": True,
        }
        UAT = Config(cfgdict=cfg)
        self.assertEqual(UAT.logfile, cfg["logfile"])
        self.assertEqual(UAT.top_req_pages, cfg["top_req_pages"])
        self.assertEqual(UAT.perc_succ_reqs, cfg["perc_succ_reqs"])
        self.assertEqual(UAT.perc_fail_reqs, cfg["perc_fail_reqs"])
        self.assertEqual(UAT.top_hosts, cfg["top_hosts"])
        self.assertEqual(UAT.top_pages_per_host, cfg["top_pages_per_host"])
        self.assertEqual(UAT.error_in_lines, cfg["error_in_lines"])

    def test_logline(self):
        legit_line = (
            'uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 10'
        )
        lg = LogLine(legit_line)
        print(lg.page)
        self.assertEqual(lg.host, "uplherc.upl.com")
        self.assertEqual(lg.time, "01/Aug/1995:00:00:07 -0400")
        self.assertEqual(lg.page, "/")
        self.assertEqual(lg.verb, "GET")
        self.assertEqual(lg.version, "HTTP/1.0")
        self.assertEqual(lg.status, 304)
        self.assertEqual(lg.nbytes, 10)

    def test_logline_missing_nbytes(self):
        legit_line = (
            'uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 '
        )
        lg = LogLine(legit_line)
        print(lg.page)
        self.assertEqual(lg.host, "uplherc.upl.com")
        self.assertEqual(lg.time, "01/Aug/1995:00:00:07 -0400")
        self.assertEqual(lg.page, "/")
        self.assertEqual(lg.verb, "GET")
        self.assertEqual(lg.version, "HTTP/1.0")
        self.assertEqual(lg.status, 304)
        self.assertEqual(lg.nbytes, 0)

    def test_logline_missing_version(self):
        legit_line = 'uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / " 304 10'
        lg = LogLine(legit_line)
        print(lg.page)
        self.assertEqual(lg.host, "uplherc.upl.com")
        self.assertEqual(lg.time, "01/Aug/1995:00:00:07 -0400")
        self.assertEqual(lg.page, "/")
        self.assertEqual(lg.verb, "GET")
        self.assertEqual(lg.status, 304)
        self.assertEqual(lg.nbytes, 10)
        self.assertEqual(lg.version, None)

    def test_logline_malformed_raises(self):
        bad_line = 'zooropa.res.cmu.edu - - [31/Aug/1995:10:36:28 -0400] "GET /htbin/cdt_clock.pl HTTP/1.0From:  <berend@blazemonger.pc.cc.cmu.edu>" 200 704'
        with self.assertRaises(ValueError):
            lg = LogLine(bad_line)

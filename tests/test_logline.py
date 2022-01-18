import unittest
from src.ireadlogs.logline import LogLine


class TestLogStats(unittest.TestCase):
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

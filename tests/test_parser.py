import unittest
from src.ireadlogs.parser import Parser


class TestLogStats(unittest.TestCase):
    def test_parse(self):
        args = Parser().parser.parse_args(
            [
                "fpath",
                "--pages",
                "10",
                "--hosts",
                "20",
                "--hosts-breakdown",
                "30",
                "--show-errors",
            ]
        )
        self.assertEqual(args.logfile, "fpath")
        self.assertEqual(args.pages, 10)
        self.assertEqual(args.hosts, 20)
        self.assertEqual(args.hosts_breakdown, 30)
        self.assertEqual(args.show_errors, True)

    def test_parse_defaults(self):
        args = Parser().parser.parse_args(["fpath"])
        self.assertEqual(args.logfile, "fpath")
        self.assertEqual(args.pages, 10)
        self.assertEqual(args.hosts, 10)
        self.assertEqual(args.hosts_breakdown, 5)
        self.assertEqual(args.show_errors, False)

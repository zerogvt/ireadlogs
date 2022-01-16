'''
This is a script that will be used in the setup.py as an entry point.
Instantiate all your classes here.
'''
import argparse
from fileinput import lineno
import sys
import re

def get_parser():
    ''' Parses command line arguments '''

    parser = argparse.ArgumentParser(description=
            "Description of the app that will be displayed when the script is executed.")
    parser.add_argument('--test', help="Test the app.", dest="test",
                        action='store_true', required=False)
    return parser


def read_log():
    p = re.compile(r'(.*)\s-\s-\s\[(.*)\]\s"(\w+)\s(.*)\s(.*)"\s(\d+)\s(\d+)?')
    lineno = 0
    hosts = {}
    errors = []
    succ = 0
    fails = 0
    lineno = 0
    with open("NASA_access_log_Aug95", "r") as logfile:
        for line in logfile:
            lineno += 1
            try:
                m = p.match(line)
                # unpack parsed values
                nbytes = 0
                if len(m.groups()) == 7:
                    host, t, verb, img, vers, status, nbytes = m.groups()
                elif len(m.groups()) == 6:
                    host, t, verb, img, vers, status = m.groups()
                else:
                    errors.append(lineno)
                    continue
                if int(status) >= 400 or int(status) < 200:
                    fails += 1
                else:
                    succ += 1
                if host not in hosts:
                    hosts[host] = 1
                else:
                    hosts[host] += 1
            except (UnicodeDecodeError, AttributeError):
                errors.append(lineno)
                continue
    hosts_freq = sorted(hosts.keys(), key=lambda x: hosts[x], reverse=True)
    print(succ, fails)
    #for h in hosts_freq[:20]:
    #    print(h, hosts[h])



def execute_script(input_args):
    parsed_args = get_parser().parse_args(input_args)
    print(parsed_args)
    if parsed_args.test:
        print("Testing the app.")
    read_log()


def main():
    # Entry point to the app. Call in test method
    execute_script(sys.argv[1:])


if __name__ == "__main__":
    main()
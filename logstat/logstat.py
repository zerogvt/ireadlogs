'''
This is a script that will be used in the setup.py as an entry point.
Instantiate all your classes here.
'''
import argparse
from fileinput import lineno
import sys
import re
import json

def get_parser():
    ''' Parses command line arguments '''

    parser = argparse.ArgumentParser(description=
            "Description of the app that will be displayed when the script is executed.")
    parser.add_argument('--test', help="Test the app.", dest="test",
                        action='store_true', required=False)
    return parser


def read_log():
    res = {
        "top_10_req_pages": [],
        "perc_succ_reqs": 0,
        "perc_fail_reqs": 0,
        "top_10_hosts": [],
        "error_in_lines": None
    }
    p = re.compile(r'(.*)\s-\s-\s\[(.*)\]\s"(\w+)\s(.*)(\s.*)?"\s(\d+)\s(\d+)?')
    lineno = 0
    hosts = {}
    pages = {}
    errors = []
    lineno = 0
    with open("NASA_access_log_Aug95", "r", errors='replace') as logfile:
        for line in logfile:
            lineno += 1
            try:
                m = p.match(line)
                # unpack parsed values
                nbytes = 0
                if len(m.groups()) == 7:
                    host, t, verb, page, vers, status, nbytes = m.groups()
                elif len(m.groups()) == 6:
                    host, t, verb, page, vers, status = m.groups()
                else:
                    errors.append(lineno)
                    continue
                if page not in pages:
                    pages[page] = { 'count': 1, 'fails': 0}
                else:
                    pages[page]['count'] += 1

                if host not in hosts:
                    hosts[host] = { 'count': 1, 'fails': 0, 'pages': { page: 1 }}
                else:
                    hosts[host]['count'] += 1
                    if page not in hosts[host]['pages']:
                        hosts[host]['pages'][page] = 1
                    else:
                        hosts[host]['pages'][page] += 1
                if int(status) >= 400 or int(status) < 200:
                    hosts[host]['fails'] += 1
                    pages[page]['fails'] += 1
            except (UnicodeDecodeError, AttributeError):
                errors.append(lineno)
                continue
    pages_freq = sorted(pages.keys(), key=lambda x: pages[x]['count'], reverse=True)
    for p in pages_freq[:10]:
        res['top_10_req_pages'].append((p, pages[p]['count']))
    
    fails, total = 0, 0
    for h in hosts:
        fails += hosts[h]['fails']
        total += hosts[h]['count']
    print(fails, total)
    succ = total - fails
    res['perc_succ_reqs'] = f"{100 * succ/total:.2f}"
    res['perc_fail_reqs'] = f"{100 * fails/total:.2f}"

    hosts_freq = sorted(hosts.keys(), key=lambda x: hosts[x]['count'], reverse=True)
    for h in hosts_freq[:10]:
        res['top_10_hosts'].append({ 'host': h , 'count': hosts[h]['count'], 'breakdown': []})
        pages_freq_for_host = sorted(hosts[h]['pages'].keys(), key=lambda x: hosts[h]['pages'][x], reverse=True)
        for p in pages_freq_for_host[:5]:
            res['top_10_hosts'][-1]['breakdown'].append((p, hosts[h]['pages'][p]))

    res['error_in_lines'] = errors
    return res


def execute_script(input_args):
    parsed_args = get_parser().parse_args(input_args)
    print(parsed_args)
    if parsed_args.test:
        print("Testing the app.")
    res = read_log()
    print(json.dumps(res, indent=4))


def main():
    # Entry point to the app. Call in test method
    execute_script(sys.argv[1:])


if __name__ == "__main__":
    main()
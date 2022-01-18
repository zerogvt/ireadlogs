# ireadlogs
This is a small python module that parses logs such as [this](ftp://ita.ee.lbl.gov/traces/NASA_access_log_Aug95.gz) 
available at [NASA-FTP](ftp://ita.ee.lbl.gov/traces/), 
and produces a JSON report with next information:
1. Top requested pages and the number of requests made for each
2. Percentage of successful requests (anything in the 200s and 300s range)
3. Percentage of unsuccessful requests (anything that is not in the 200s or 300s range)
4. Top 10 unsuccessful page requests
5. The top 10 hosts making the most requests, displaying the IP address and number of
requests made.
6. For each of the top hosts, show the top 5 pages requested and the number of
requests for each page
7. The log file contains malformed entries; for each malformed line, display an error
message and the line number.

Command line options may alter the produced results with regards to the number of top hosts and pages, 
the top hosts - pages breakdown and the reporting of errors.

# Prerequisites
You need [python > 3.8](https://www.python.org/downloads/) [virtualenv](https://pypi.org/project/virtualenv/) installed in your system.

# Installation
Create a python virtual environment 
`virtualenv -p $(which python3) venv`

Activate it
`. venv/bin/activate`

Install ireadlogs from pypa:
`pip install ireadlogs -U`

Run:
`python -m ireadlogs path_to_logfile`

# Getting help / Command line options
```
python -m ireadlogs -h
usage: __main__.py [-h] [--pages PAGES] [--hosts HOSTS]
                   [--hosts-breakdown HOSTS_BREAKDOWN] [--show-errors]
                   logfile

positional arguments:
  logfile

optional arguments:
  -h, --help            show this help message and exit
  --pages PAGES         limits the top pages shown (default is 10)
  --hosts HOSTS         limits the top hosts shown (default is 10)
  --hosts-breakdown HOSTS_BREAKDOWN
                        limits the top pages per host breakdown (default is 5)
  --show-errors         if present show malformed line numbers
```

# Build / Distribute
`make distribute`

# Run tests
`make test`

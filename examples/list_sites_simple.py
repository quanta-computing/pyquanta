import json
import sys

from pyquanta import Quanta

def main(creds_file, url):
    quanta = Quanta(url=url)
    with open(sys.argv[1]) as creds:
        quanta.connect(*creds.read().rstrip().split())
    sites = quanta.sites.list()
    for site in sites:
        print("{} - {} [{}]"
            .format(site.id, site.name, site.role))


def usage():
    print("Usage: list_sites_simple.py <credentials_file> [url]")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    creds_file = sys.argv[1]
    if len(sys.argv) > 2:
        url = sys.argv[2]
    else:
        url = 'https://staging.quanta.gr/api'
    main(creds_file, url)

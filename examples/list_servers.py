import json
import sys

from pyquanta import Quanta

def main(creds_file, site_id, url):
    quanta = Quanta(url=url)
    with open(sys.argv[1]) as creds:
        quanta.connect(*creds.read().rstrip().split())
    quanta.use_site(site_id)
    srvs = quanta.servers.list()
    print('Servers for site {}:'.format(site_id))
    for srv in srvs:
        print('- {} ({})'.format(srv.name, srv.role))


def usage():
    print("Usage: list_servers.py <credentials_file> <id> [url]")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
    creds_file = sys.argv[1]
    site_id = int(sys.argv[2])
    if len(sys.argv) > 3:
        url = sys.argv[3]
    else:
        url = 'https://staging.quanta.gr/api'
    main(creds_file, site_id, url)

import json
import sys

from pyquanta import Quanta

def main(creds_file, site_id, name, host, role, url):
    quanta = Quanta(url=url)
    with open(sys.argv[1]) as creds:
        quanta.connect(*creds.read().rstrip().split())
    quanta.use_site(site_id)
    s = quanta.servers.create(name=name, host=host, role=role)
    srvs = quanta.servers.list()
    print('Servers for site {}:'.format(site_id))
    for srv in srvs:
        print('- {} ({})'.format(srv.name, srv.role))


def usage():
    print("Usage: create_server.py <credentials_file> <site_id> <name> <host> <role> [url]")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
    creds_file = sys.argv[1]
    site_id = int(sys.argv[2])
    name = sys.argv[3]
    host = sys.argv[4]
    role = sys.argv[5]
    if len(sys.argv) > 6:
        url = sys.argv[6]
    else:
        url = 'https://staging.quanta.gr/api'
    main(creds_file, site_id, name, host, role, url)
